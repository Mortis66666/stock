const { MongoClient } = require('mongodb');

const db_url = process.env.MONGO_URL; // Gets the url in env
const client = new MongoClient(db_url); // Mongoclient

// Time units
const DAY = 1000 * 60 * 60 * 24; // Day in milliseconds
const SECONDS = 1000; // Seconds in milliseconds


async function get_user_info (username) {
    try {
        await client.connect() // Connect to the client
        var profiles = client.db("stocks").collection("profiles"); // Gets collection "profile"
        var result = await profiles.findOne(
            {
                "username": username
            }
        );
        return result;
    }

    catch (error) {
        return null;
    }

    finally {
        await client.close();
    }
}

async function add_coins (username, amount) {
    try {
        await client.connect()
        var profiles = client.db("stocks").collection("profiles");

        profiles.updateOne(
            {
                "username": username
            },
            {
                "$inc": {
                    "coins": amount
                }
            }
        )

    }

    finally {
        await client.close()
    }
}