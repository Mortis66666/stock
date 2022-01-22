const {MongoClient} = require('mongodb');

const db_url = process.env.MONGO_URL;
const client = new MongoClient(db_url);


async function get_bal (username) {
    try {
        await client.connect() // Connect to the client

        const profiles = client.db("stocks").collection("profiles"); // Gets collection "profile"
        var result = profiles.findOne(
            {
                username: username
            }
        )
    }


    finally {
        await client.close();
    }
}