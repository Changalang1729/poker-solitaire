import React, { useState, useEffect } from "react";

import {
  Stack,
  Box,
  RangeSelector,
  Text,
  CheckBoxGroup,
  Button,
  Anchor,
  Menu,
} from "grommet";

const styles = {
  custom: 0,
  straight: 1,
  flush: 2,
  pair: 3,
  "two-pair": 4,
  trips: 5,
  boat: 6,
  quads: 7,
  royal: 8,
  "straight-flush": 9,
};

function _updateRange(setValues, values) {
  setValues(values);
}

function _updateSuits(setSuits, suits) {
  setSuits(suits.value);
}

function SelectorRange(props) {
  const [values, setValues] = useState(props.range);
  const [suits, setSuits] = useState(props.options);

  useEffect(() => {
    props.onChange(props.index, values, suits);
  }, [values, suits, props]);

  return (
    <Box background="light-1" margin="small">
      <Box margin="small" alignContent="end" justify="end">
        <Anchor
          label="x"
          alignSelf="end"
          justify="end"
          onClick={() => props.removeItem(props.index)}
        />
      </Box>
      <Stack margin="small">
        <Box direction="row" justify="between">
          {["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"].map((value) => (
            <Box key={value} pad="small" border={false}>
              <Text style={{ fontFamily: "monospace" }}>{value}</Text>
            </Box>
          ))}
        </Box>
        <RangeSelector
          direction="horizontal"
          invert={false}
          min={1}
          max={13}
          size="full"
          round="small"
          values={values}
          onChange={_updateRange.bind(null, setValues)}
        />
      </Stack>
      <CheckBoxGroup
        margin="small"
        direction="row"
        justify="evenly"
        options={["D", "C", "H", "S"]}
        values={props.options}
        onChange={_updateSuits.bind(null, setSuits)}
      />
    </Box>
  );
}

function _updateState(setSelected, selected, index, values, suits) {
  if (selected && selected[index]) {
    selected[index].vals = values;
    selected[index].suits = suits;
    setSelected(selected);
  }
}

function _removeItem(setSelected, selected, index) {
  var temp = selected.slice(0);
  temp.splice(index, 1);
  setSelected(temp);
}

function _addRange(setSelected, selected) {
  setSelected(selected.concat([{ vals: [3, 7], suits: [] }]));
}

// These correspond to the enum up there
const menuOptions = [
  "Custom",
  "Straight",
  "Flush",
  "Pair",
  "Two Pair",
  "Trips",
  "Boat",
  "Quads",
  "Royal",
  "Straight Flush",
];

export default function CardSelector(props) {
  const [selected, setSelected] = useState([{ vals: [3, 7], suits: [] }]);
  const [gamestyle, setGamestyle] = useState(styles.custom);

  const ss = (v) => {
    setSelected(v);
    props.onChange(v);
  };

  return (
    <Box>
      <Box background="light-1" margin="small">
        <Menu
          label="Strategy"
          items={menuOptions.map((o, ind) => {
            return {
              label: o,
              onClick: () => {
                setGamestyle(ind);
              },
            };
          })}
        />
      </Box>
      <Box background="light-2" margin="small">
        Selected strategy: {menuOptions[gamestyle]}
      </Box>
      {gamestyle == styles.custom && (
        <div>
          {selected.map((obj, i) => {
            return (
              <SelectorRange
                index={i}
                key={i}
                range={obj.vals}
                options={obj.suits}
                onChange={_updateState.bind(null, ss, selected)}
                removeItem={_removeItem.bind(null, ss, selected)}
              />
            );
          })}
          <Button
            alignSelf="center"
            primary
            label="+"
            margin="small"
            onClick={() => _addRange(ss, selected)}
          />
        </div>
      )}
    </Box>
  );
}
