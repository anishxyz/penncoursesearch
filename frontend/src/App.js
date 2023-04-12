import React from 'react';
import {ChakraProvider, extendTheme} from '@chakra-ui/react';
import Homepage from "./Homepage";
import { Helmet } from "react-helmet";

const theme = extendTheme({
  config: {
    initialColorMode: "dark",
    useSystemColorMode: false,
  },
});

function App() {
  return (
    <ChakraProvider theme={theme}>
      <div>
        <Homepage />
      </div>
    </ChakraProvider>
  );
}

export default App;
