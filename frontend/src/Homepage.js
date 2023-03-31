import React, {useState} from "react";
import {useEffect} from "react";
import {
    Box,
    Center,
    Container, Flex,
    Heading,
    Input,
    Text, useColorMode,
    VStack,
} from "@chakra-ui/react";
import ColorModeSwitcher from "./ColorModeSwitcher";
import axios from 'axios';

const ResultCard = ({ title, description }) => {
  return (
    <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="4" boxShadow="md">
      <VStack align="start" spacing={2}>
        <Text fontWeight="bold" fontSize="xl">
          {title}
        </Text>
        <Text>{description}</Text>
      </VStack>
    </Box>
  );
};

const Homepage = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const {toggleColorMode} = useColorMode();
    const [searchResults, setSearchResults] = useState("");

    const handleSearch = (e) => {
        e.preventDefault();
        // Implement your search logic here
        console.log("Search term:", searchTerm);
        fetchData(searchTerm);
        setSearchTerm("");
    };

    const fetchData = async (searchTerm) => {
        console.log("here")
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/search`, {
                params: {
                    q: searchTerm,
                },
            });
            console.log(response.data);
            setSearchResults(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === "m" && e.target.tagName !== "INPUT") {
                toggleColorMode();
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [toggleColorMode]);

    return (
        <Container
            minHeight="100vh"
            display="flex"
            flexDirection="column"
            justifyContent="space-between"
        >
            <ColorModeSwitcher/>
            <Box></Box>
            <VStack>
                <Heading
                    mb="6"
                    bgGradient="linear(to-r, orange.500, yellow.500)"
                    bgClip="text"
                    textAlign="center"
                >
                    Penn Course Search
                </Heading>
                <Flex flexDirection="column" alignItems="center">
                    <Center>
                        <form onSubmit={handleSearch}>
                            <Input
                                size="lg"
                                placeholder="I want to learn about..."
                                variant="filled"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </form>
                    </Center>
                </Flex>
                <Box pt="10" w="100%">
                    {searchResults && (
                        <ResultCard title="Search Result" description={searchResults}/>
                    )}
                </Box>
            </VStack>
            <Box>
                <Text textAlign="center" fontSize="sm" pb={4}>
                    Built by Anish Agrawal
                </Text>
            </Box>
        </Container>
    );
}

export default Homepage;