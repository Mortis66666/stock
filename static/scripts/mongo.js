const {MongoClient} = require('mongodb');
const db_url = process.env.MONGO_URL;

const client = new MongoClient(db_url);


async function main () {
    try {
        const profiles = client.db("stocks").collection("profiles");
    }
    finally {
        await client.close();
    }
}