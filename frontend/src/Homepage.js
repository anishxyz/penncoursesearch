import React, {useState} from "react";
import {useEffect} from "react";
import {
    Box,
    Center,
    Container, Flex,
    Heading,
    Input,
    Text, useColorMode,
    VStack,  IconButton,
} from "@chakra-ui/react";
import {Icon, InfoIcon} from "@chakra-ui/icons";
import ColorModeSwitcher from "./ColorModeSwitcher";
import InfoModal from "./InfoModal";
import axios from 'axios';
import { FaBolt } from "react-icons/fa";
import ResultCard from "./ResultCard";
import FastResultCard from "./FastResultCard";
import LoadingCard from "./LoadingCard";


const Homepage = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const {toggleColorMode} = useColorMode();
    const {colorMode} = useColorMode();
    const [searchResults, setSearchResults] = useState("");
    const [lastSearchTerm, setLastSearchTerm] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
    const [fastSearchResults, setFastSearchResults] = useState([]);

    const handleSearch = (e) => {
        e.preventDefault();
        // Implement your search logic here
        console.log("Searching for: " + searchTerm)
        setFastSearchResults([]);
        fetchData(searchTerm);
        setLastSearchTerm(searchTerm);
        setSearchTerm("");
    };

    const fetchData = async (searchTerm) => {
        setIsLoading(true);
        console.log("Fetching courses....")
        try {
            // console.log(`${process.env.REACT_APP_API_URL}/searchfast`);
            const fastResponse = await axios.get(`${process.env.REACT_APP_API_URL}/searchfast`, {
                params: {
                    q: searchTerm,
                },
            });

            const fastCourses = fastResponse.data.courses;
            const context = fastResponse.data.context;

            setFastSearchResults(fastCourses);

            // console.log(`${process.env.REACT_APP_API_URL}/search`)
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/search`, {
                q: searchTerm,
                context: context
            });

            // console.log(response.data);

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

    const openInfoModal = () => {
        setIsInfoModalOpen(true);
    };

    const closeInfoModal = () => {
        setIsInfoModalOpen(false);
    };

    return (
        <Container
            minHeight="100vh"
            display="flex"
            flexDirection="column"
            justifyContent="space-between"
            p={{base: 4, md: 0}}
            maxW={{base: "90%", md: "container.md"}}
        >
            <Flex position="fixed" top={4} right={4} align="center">
                <IconButton
                    icon={<InfoIcon/>}
                    colorScheme="orange"
                    onClick={openInfoModal}
                    position="fixed"
                    top="1rem"
                    right="4rem" // Adjust this value according to your needs
                    zIndex="2"
                    aria-label="Info"
                />
                <ColorModeSwitcher/>
            </Flex>
            <InfoModal isOpen={isInfoModalOpen} onClose={closeInfoModal}/>
            <Box></Box>
            <VStack>
                <Heading
                    pt={{ base: "4rem", md: "6rem" }} // Adjust the padding-top value for different screen sizes
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
                                    boxShadow: colorMode === "dark" ? '0 0 0 1px orange' : 'none',
                                }}
                            />
                        </form>
                    </Center>
                </Flex>
                <Box pt="10" w="100%">
                    <VStack spacing={4} alignItems="center">
                        {isLoading ? (
                            <LoadingCard/>
                        ) : searchResults ? (
                            <ResultCard title={lastSearchTerm} description={searchResults}/>
                        ) : null}
                        {fastSearchResults.length > 0 && (
                            <Box
                                w="100%" // Add this to set the width
                                style={{
                                    overflow: "scroll",
                                    scrollSnapType: "y mandatory", // Add this for scroll snapping
                                }}
                            >
                                <FastResultCard courses={fastSearchResults}/>
                            </Box>
                        )}
                    </VStack>
                </Box>
            </VStack>
            <Box>
                <Text textAlign="center" fontSize="sm" pb={4} pt={10}>
                    Built by Anish Agrawal
                </Text>
            </Box>
        </Container>
    );
}

export default Homepage;