import React, {useState} from "react";
import {useEffect} from "react";
import {
    Box,
    Center,
    Container, Flex,
    Heading,
    Input,
    Text, useColorMode,
    VStack, Skeleton, Stack
} from "@chakra-ui/react";
import ColorModeSwitcher from "./ColorModeSwitcher";
import axios from 'axios';

const ResultCard = ({title, description}) => {
    return (
        <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="4" boxShadow="md">
            <VStack align="start" spacing={2}>
                <Text fontWeight="bold" fontSize="xl">
                    {title}
                </Text>
                <Text
                    style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}
                >
                    {description}
                </Text>
            </VStack>
        </Box>
    );
};

const LoadingCard = () => {
    return (
        <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="4" boxShadow="md">
            <Stack>
                <Skeleton height='20px'/>
                <Skeleton height='20px'/>
                <Skeleton height='20px'/>
            </Stack>
        </Box>
  );
};

const Homepage = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const {toggleColorMode} = useColorMode();
    const [searchResults, setSearchResults] = useState("");
    const [lastSearchTerm, setLastSearchTerm] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = (e) => {
        e.preventDefault();
        // Implement your search logic here
        console.log("searching for: " + searchTerm)
        fetchData(searchTerm);
        setLastSearchTerm(searchTerm);
        setSearchTerm("");
    };

    const fetchData = async (searchTerm) => {
        setIsLoading(true);
        console.log("fetching data....")
        try {
            console.log(`${process.env.REACT_APP_API_URL}/search`)
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/search`, {
                params: {
                    q: searchTerm,
                },
            });
            console.log(response.data);
            setSearchResults(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setIsLoading(false);
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
            p={{ base: 4, md: 0 }}
            maxW={{ base: "90%", md: "container.md" }}
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
                                focusBorderColor="orange"
                                _focus={{
                                    boxShadow: '0 0 0 1px orange',
                                }}
                            />
                        </form>
                    </Center>
                </Flex>
                <Box pt="10" w="100%">
                    {isLoading ? (
                        <LoadingCard/>
                    ) : searchResults ? (
                        <ResultCard title={lastSearchTerm} description={searchResults}/>
                    ) : null}
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