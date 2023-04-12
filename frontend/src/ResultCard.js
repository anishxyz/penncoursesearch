import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  useColorModeValue,
  Divider,
  Heading,
} from "@chakra-ui/react";
import { Icon } from "@chakra-ui/icons";
import { FaMagic } from "react-icons/fa";

const ResultCard = ({ title, description }) => {
  const borderColor = useColorModeValue("gray.300", "whiteAlpha.400");
  const bgColor = useColorModeValue("gray.100", "gray.700");

  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      overflowY="scroll"
      maxH="400px"
      p="4"
      boxShadow="md"
      bgColor={bgColor}
      w="100%"
      border="2px solid"
      borderColor="orange.500"
    >
      <VStack align="start" spacing={4}>
        <Icon as={ FaMagic } boxSize="1.5rem" color="orange.500" mr={2} />
        <Heading size="sm" mb="1">
          {title}
        </Heading>
        <Divider borderColor={borderColor} borderRadius="full" />
        <Text style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
          {description}
        </Text>
      </VStack>
    </Box>
  );
};

export default ResultCard;
