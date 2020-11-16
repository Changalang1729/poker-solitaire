import React, { useState, useEffect, useRef } from "react";

import "../styles/landing.css";
import { Main, Heading, Grid, Box } from "grommet";

import Card from "../components/card";
import CardSelector from "../components/cardSelector";

function Blob1() {
  return (
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <path
        fill="#FF0066"
        d="M60.4,-42.1C76.6,-27.8,87,-2.8,83,20.6C79,44,60.6,65.8,38.8,73.5C17.1,81.2,-7.9,74.8,-28.1,63.2C-48.2,51.6,-63.4,34.8,-63.1,19.3C-62.7,3.8,-46.7,-10.4,-33.6,-24C-20.5,-37.6,-10.3,-50.7,5.9,-55.4C22.1,-60.1,44.1,-56.4,60.4,-42.1Z"
        transform="translate(100 100)"
      />
    </svg>
  );
}

export default function Game() {
  const cardList = useRef();

  const update = (selected) => {
    let cardsChosen = new Set();

    selected.forEach((obj) => {
      obj.suits.forEach((suit) => {
        for (var i = obj.vals[0]; i <= obj.vals[1]; i++) {
          cardsChosen.add(`${i}${suit.toLowerCase()}`);
        }
      });
    });

    let cl = Array.from(cardsChosen);
    cardList.current = cl;
    console.log(cardList.current);

    _runGame(cl);
  };

  return (
    <Main align="stretch">
      <Grid
        rows={["xsmall", "flex"]}
        columns={["flex", "large"]}
        gap="xsmall"
        alignSelf="stretch"
        fill="horizontal"
        areas={[
          { name: "header", start: [0, 0], end: [1, 0] },
          { name: "options", start: [1, 1], end: [1, 1] },
          { name: "main", start: [0, 1], end: [0, 1] },
        ]}
      >
        <Box
          gridArea="header"
          align="center"
          justify="center"
          background="brand"
          flex={true}
        >
          <Heading alignSelf="center">Poker Solitaire</Heading>
        </Box>
        <Box gridArea="main" background="light-2" flex={true} />
        <Box gridArea="options" background="light-5" flex={true}>
          <CardSelector onChange={update} />
        </Box>
      </Grid>
    </Main>
  );
}

const _runGame = async (cardList) => {
  const response = await fetch("http://127.0.0.1:5000/poker/desiredCards", {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify({ desiredCards: ["Th", "A", "K", "Q", "J"] }), // body data type must match "Content-Type" header
  });
  var res = await response.json();
  console.log(res);
  return res;
};
