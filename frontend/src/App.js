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
          <meta property="og:description" content="An AI powered search engine for the UPenn course catalog" />
          <meta property="og:image" content={`${process.env.PUBLIC_URL}/previewImage.png`} />
          <meta property="og:url" content={`${process.env.REACT_APP_API_URL}`} />
          <meta property="og:type" content="website" />
        </Helmet>
        <Homepage />
      </div>
    </ChakraProvider>
  );
}

export default App;
