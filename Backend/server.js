require("dotenv").config();
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const crypto = require("crypto");
const {
    Client, PrivateKey, AccountId,
    TopicCreateTransaction, TopicMessageSubmitTransaction,
    TopicMessageQuery, TopicInfoQuery, Timestamp
} = require("@hashgraph/sdk");

const app = express();
const PORT = 3000;
app.use(bodyParser.json());

// Setup Hedera client
const myAccountId = AccountId.fromString(process.env.MY_ACCOUNT_ID);
const myPrivateKey = PrivateKey.fromStringECDSA(process.env.MY_PRIVATE_KEY);
const client = Client.forTestnet().setOperator(myAccountId, myPrivateKey);

// Path to mapping file
const MAPPING_FILE = "userTopicMap.json";

// Load existing mappings from file
let userHashToTopicIdMap = {};
if (fs.existsSync(MAPPING_FILE)) {
    try {
        userHashToTopicIdMap = JSON.parse(fs.readFileSync(MAPPING_FILE, "utf8"));
    } catch (e) {
        console.error("❌ Failed to parse mapping file:", e);
        userHashToTopicIdMap = {};
    }
}

// Save mapping to disk
function saveMappingToFile() {
    fs.writeFileSync(MAPPING_FILE, JSON.stringify(userHashToTopicIdMap, null, 2), "utf8");
}

// Hash a string using SHA-256
function hashString(input) {
    return crypto.createHash("sha256").update(input.trim()).digest("hex");
}

// Create topic and store data
const createTopicAndStore = async (data, userHash) => {
    try {
        const topicTx = await new TopicCreateTransaction()
            .setAdminKey(myPrivateKey.publicKey)
            .setAutoRenewAccountId(myAccountId)
            .execute(client);

        const receipt = await topicTx.getReceipt(client);
        const topicId = receipt.topicId.toString();

        await new TopicMessageSubmitTransaction()
            .setTopicId(topicId)
            .setMessage(Buffer.from(JSON.stringify(data), "utf8"))
            .execute(client);

        userHashToTopicIdMap[userHash] = topicId;
        saveMappingToFile(); // Persist mapping

        return topicId;
    } catch (error) {
        console.error("❌ Error creating topic:", error);
        throw error;
    }
};

// Endpoint to store data
app.post("/store-data", async (req, res) => {
    const {
        email,
        otp,
        userHash,
        combinedHash,
        chaoticKeys,
        regions
    } = req.body;

    if (!email || !otp || !userHash || !combinedHash || !Array.isArray(chaoticKeys) || !Array.isArray(regions)) {
        return res.status(400).json({ error: "Missing or invalid fields in request" });
    }

    const topicData = {
        email,
        otp,
        userHash: userHash.trim(),
        combinedHash,
        chaoticKeys,
        regions
    };

    try {
        const topicId = await createTopicAndStore(topicData, userHash.trim());
        res.json({ message: "✅ Data stored on Hedera successfully", topicId });
    } catch (err) {
        console.error("❌ Hedera store error:", err);
        res.status(500).json({ error: "❌ Failed to store on Hedera", details: err.message });
    }
});

// Endpoint to retrieve data based on password
app.get("/get-data", async (req, res) => {
    const { password } = req.query;

    if (!password) {
        return res.status(400).json({ error: "Missing password" });
    }

    const passwordHash = hashString(password);
    console.log("🔐 Computed passwordHash:", passwordHash);

    const topicId = userHashToTopicIdMap[passwordHash];
    if (!topicId) {
        return res.status(404).json({ error: "❌ Topic ID not found for given password" });
    }

    try {
        const topicInfo = await new TopicInfoQuery()
            .setTopicId(topicId)
            .execute(client);

        if (topicInfo.sequenceNumber.toNumber() === 0) {
            return res.status(404).json({ error: "❌ Topic exists but contains no messages" });
        }

        const result = await new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error("⏰ Timeout while waiting for message"));
            }, 30000);

            const subscription = new TopicMessageQuery()
                .setTopicId(topicId)
                .setStartTime(Timestamp.fromDate(new Date(Date.now() - 60000))) // 60s buffer
                .subscribe(
                    client,
                    (error) => {
                        clearTimeout(timeout);
                        subscription.unsubscribe();
                        reject(error || new Error("❌ Subscription error"));
                    },
                    (message) => {
                        const raw = Buffer.from(message.contents, "utf8").toString();
                        console.log("📩 Received message:", raw);

                        try {
                            const decoded = JSON.parse(raw);
                            if (decoded.userHash === passwordHash) {
                                clearTimeout(timeout);
                                subscription.unsubscribe();
                                resolve(decoded);
                            } else {
                                console.warn("❌ Password hash mismatch");
                            }
                        } catch (err) {
                            console.warn("❌ Failed to parse message:", err);
                        }
                    }
                );
        });

        return res.status(200).json(result);
    } catch (err) {
        console.error("❌ Error retrieving data:", err);
        return res.status(500).json({ error: `❌ Failed to retrieve data: ${err.message}` });
    }
});

app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
