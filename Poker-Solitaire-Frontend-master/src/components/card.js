import React from "react";
import styled, { css } from "styled-components";

const CardContainer = styled.div`
  height: 95px;
  width: 72px;
  perspective: 100px;
  margin: 5px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 5px;
  border-style: solid;
  font-family: "Bebas Neue";
  ${(props) =>
    props.red &&
    css`
      color: red;
    `};
`;

const CardVal = styled.div`
  margin: 5px;
  font-size: 44px;
  flex: 1;
  padding-top: 7px;
`;

const CardSuit = styled.div`
  font-size: 44px;
  padding-top: 20px;
  padding-right: 5px;
  padding-bottom: 2px;
  flex: 1;
  text-align: right;
`;

const Card = ({ val, suit }) => {
  return (
    <CardContainer red={suit == "H" || suit == "D"}>
      <CardVal>{val}</CardVal>
      <CardSuit>{suit}</CardSuit>
    </CardContainer>
  );
};

const SuitIcon = ({ suit }) => {
  // TODO: suit icon
  return <></>;
};

export default Card;
