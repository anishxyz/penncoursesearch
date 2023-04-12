import {Box, Divider, Heading, Text, useColorModeValue, VStack} from "@chakra-ui/react";
import {Icon} from "@chakra-ui/icons";
import {FaBolt} from "react-icons/fa";
import React from "react";

const FastResultCard = ({ courses }) => {
  const borderColor = useColorModeValue("gray.300", "whiteAlpha.400");
  const bgColor = useColorModeValue("gray.100", "gray.700");

  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      overflowY="scroll"
      maxH="600px"
      p="4"
      boxShadow="md"
      bgColor={bgColor}
      w="100%"
    >
      <VStack align="start" spacing={4}>
        <Icon as={FaBolt} boxSize="1.5rem" color="orange.500" />
        {courses.map((course, index) => (
          <React.Fragment key={index}>
            {index !== 0 && (
              <Divider borderColor={borderColor} borderRadius="full" />
            )}
            <Box>
              <Heading size="sm" mb="1">
                {course.title}
              </Heading>
              <Text style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
                {course.description}
              </Text>
            </Box>
          </React.Fragment>
        ))}
      </VStack>
    </Box>
  );
};

export default FastResultCard;