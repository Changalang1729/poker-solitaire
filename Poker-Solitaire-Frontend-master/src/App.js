import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Grommet } from "grommet";

import Landing from "./pages/Landing";

const theme = {
  global: {
    font: {
      family: "Poppins",
      size: "18px",
      height: "20px",
    },
  },
};

function App() {
  return (
    <Grommet full theme={theme}>
      <Landing />
    </Grommet>
  );
}

export default App;
