
async function translateText(text) {
  const response = await fetch("http://localhost:5000/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const data = await response.json();
  return data.translatedText;
}


function findTextNodes(element) {
  let textNodes = [];
  for (let node of element.childNodes) {
    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== "") {
      textNodes.push(node);
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      textNodes = textNodes.concat(findTextNodes(node));
    }
  }
  return textNodes;
}


async function translatePage() {
  const textNodes = findTextNodes(document.body);

  for (const node of textNodes) {
    const originalText = node.textContent.trim();
    if (originalText) {
      try {
        const translatedText = await translateText(originalText);
        node.textContent = translatedText;
      } catch (error) {
        console.error("Translation failed:", error);
      }
    }
  }
}


translatePage();