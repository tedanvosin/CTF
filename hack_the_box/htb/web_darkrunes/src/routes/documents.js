const sanitizeHtml = require("sanitize-html");
const { signString } = require("../utils/crypto");
const {
  findUserDocuments,
  findDocument,
  deleteDocument,
  addDocument,
} = require("../database");
const { isAuthenticated } = require("../middlewares");

const router = require("express").Router();

router.post("/documents", isAuthenticated, (req, res) => {
  const { content } = req.body;
  const user = req.user;

  if (!content || typeof content !== "string") {
    return res.send("Bad document content oO, make sure it's not empty");
  }

  /**
   * @dev  Allow users to give links for external content in their documents for future references
   */
  const sanitizedContent = sanitizeHtml(content, {
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      a: ["style"],
    },
  });

  const integrity = signString(content);
  addDocument(user.id, sanitizedContent, integrity);
  return res.redirect(`/documents`);
});

router.get("/documents", isAuthenticated, (req, res) => {
  const user = req.user;
  const documents = findUserDocuments(user.id);

  res.render("documents", { documents });
});

router.post("/document/:id/delete", isAuthenticated, (req, res) => {
  const { id } = req.params;
  const user = req.user;

  const document = findDocument(id, user.id);
  if (!document) {
    return res.status(404).send("Document not found");
  }

  deleteDocument(id);

  res.redirect("/documents");
});

router.get("/documents/new", isAuthenticated, (req, res) => {
  res.render("create-document");
});

router.get("/document/:id", isAuthenticated, (req, res) => {
  const { id } = req.params;

  const user = req.user;
  const document = findDocument(user.id, id);

  if (!document) {
    return res.status(404).send("Document not found");
  }

  res.set("Content-Type", "text/html");
  return res.send(document.content);
});

module.exports = router;
