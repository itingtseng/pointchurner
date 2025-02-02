import fetch from "node-fetch";
import cron from "node-cron";

const urls = [
  "https://your-airbnb-clone-url/",
  "https://your-group-project-url/",
  "https://your-capstone-url/"
];

// Schedule the task to run every 10 minutes during working hours (7 AM - 7 PM, Mon-Fri)
cron.schedule("*/10 7-19 * * 1-5", async () => {
  console.log("Pinging sites...");

  for (const url of urls) {
    try {
      const res = await fetch(url);
      console.log(`Pinged ${url}: ${res.status}`);
    } catch (error) {
      console.error(`Error pinging ${url}:`, error.message);
    }
  }
});

console.log("Cron job started...");
