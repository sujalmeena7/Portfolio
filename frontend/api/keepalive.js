export default async function handler(req, res) {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  if (!backendUrl) {
    return res.status(500).json({ error: "No backend URL configured" });
  }

  try {
    const response = await fetch(`${backendUrl}/health`);
    if (response.ok) {
      return res.status(200).json({ status: "ok", message: "Pinged HF Space successfully" });
    }
    return res.status(502).json({ error: "HF Space returned error" });
  } catch (err) {
    return res.status(500).json({ error: "Failed to ping HF Space", details: err.message });
  }
}
