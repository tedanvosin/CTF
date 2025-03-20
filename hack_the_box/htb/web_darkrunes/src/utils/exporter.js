var markdownpdf = require("markdown-pdf");

const generatePDF = async (content) => {

  return new Promise((resolve, reject) => {
    markdownpdf({ remarkable: { html: true } })
      .from.string(content)
      .to.buffer(undefined, (err, buffer) => {
        if (err != null) return reject(err);
        return resolve(buffer);
      });
  });
};

module.exports = { generatePDF };
