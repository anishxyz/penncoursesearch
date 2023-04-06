import React, {useState} from "react";
import {useEffect} from "react";
import {
    Box,
    Center,
    Container, Flex,
    Heading,
    Input,
    Text, useColorMode,
    VStack, Skeleton, Stack, IconButton
} from "@chakra-ui/react";
import { InfoIcon } from "@chakra-ui/icons";
import ColorModeSwitcher from "./ColorModeSwitcher";
import InfoModal from "./InfoModal";
import axios from 'axios';

const ResultCard = ({ title, description }) => {
  const [transform, setTransform] = useState('perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)');
  const aggr = 70; // increase to make more subtle, decrease for more jumpy

  const calc = (x, y) => [
    -(y - window.innerHeight / 2) / aggr,
    (x - window.innerWidth / 2) / aggr,
    1.05,
  ];

  const trans = (x, y, s) => `perspective(1000px) rotateX(${x}deg) rotateY(${y}deg) scale(${s})`;

  const handleMouseMove = (e) => {
    const [x, y, s] = calc(e.clientX, e.clientY);
    setTransform(trans(x, y, s));
  };

  const handleMouseLeave = () => {
    setTransform('perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)');
  };

  return (
    <div
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ transform }}
    >
      <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p="4" boxShadow="md">
        <VStack align="start" spacing={2}>
          <Text fontWeight="bold" fontSize="xl">
            {title}
          </Text>
          <Text style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
            {description}
          </Text>
        </VStack>
      </Box>
    </div>
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
    const { colorMode } = useColorMode();
    const [searchResults, setSearchResults] = useState("");
    const [lastSearchTerm, setLastSearchTerm] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);

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
            p={{ base: 4, md: 0 }}
            maxW={{ base: "90%", md: "container.md" }}
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
            <InfoModal isOpen={isInfoModalOpen} onClose={closeInfoModal} />
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
                                    boxShadow: colorMode === "dark" ? '0 0 0 1px orange' : 'none',
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