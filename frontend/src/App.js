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
        <Helmet>
          <title>Penn Course Search</title>
          <meta property="og:title" content="Penn Course Search" />
          <meta name="description" property="og:description" content="An AI powered search engine for the UPenn course catalog" />
          <meta name="image" property="og:image" content="https://penncoursesearch.herokuapp.com/previewImage.jpg" />
          <meta property="og:url" content="https://penncoursesearch.herokuapp.com" />
          <meta property="og:type" content="website" />
        </Helmet>
        <Homepage />
      </div>
    </ChakraProvider>
  );
}

export default App;
