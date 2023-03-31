import React from 'react';
import {ChakraProvider, extendTheme} from '@chakra-ui/react';
import Homepage from "./Homepage";

const theme = extendTheme({
  config: {
    initialColorMode: "dark",
    useSystemColorMode: false,
  },
});

function App() {
  return (
    <ChakraProvider>
      <Homepage />
    </ChakraProvider>
  );
}

export default App;
