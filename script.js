import fetch from "node-fetch";
import { JSDOM } from "jsdom";

async function getVariableValue(url, variableName) {
  try {
    // Fetch the HTML content of the website
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}, status ${response.status}`);
    }

    const html = await response.text();
    const dom = new JSDOM(html);

    // Get all script tags
    const scripts = dom.window.document.querySelectorAll("script");

    // Iterate through each script tag
    for (let i = 0; i < scripts.length; i++) {
      const script = scripts[i];

      // Extract the text content of the script tag
      const scriptContent = script.textContent;

      // Use regular expressions to find the variable and its value
      const regex = new RegExp(`const\\s+${variableName}\\s*=\\s*([^;]+);`);
      const match = scriptContent.match(regex);

      // If the variable is found, return its value
      if (match) {
        return match[1].trim();
      }
    }

    // If the variable was not found, return null
    return null;
  } catch (error) {
    console.error("Error:", error.message);
    return null;
  }
}

// Example usage
const url = "https://www.argentina.gob.ar/interior/feriados-nacionales-2024";
const variableName = "holidays2024";

getVariableValue(url, variableName)
  .then((value) => {
    if (value !== null) {
      console.log(`The value of ${variableName} is: ${value}`);
    } else {
      console.log(`Variable ${variableName} not found on the webpage.`);
    }
  })
  .catch((error) => console.error("Error:", error));
