// import React from "react";
// import App from "./components/App";
// import "./index.css";
// import { createRoot } from "react-dom/client";

// const container = document.getElementById("root");
// const root = createRoot(container);
// root.render(<App />);
import React from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom"

import { router } from "./router"
import "./index.css";

const rootContainer = document.getElementById("root")
const root = createRoot(rootContainer)
root.render(
  <RouterProvider router={router} />
);