import {Box, Skeleton, Stack} from "@chakra-ui/react";
import React from "react";

const LoadingCard = () => {
  return (
    <Box
      w="100%" // Set the width to 100%
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      p="4"
      boxShadow="md"
    >
      <Stack>
        <Skeleton height="20px" />
        <Skeleton height="20px" />
        <Skeleton height="20px" />
        <Skeleton height="20px" />
      </Stack>
    </Box>
  );
};

export default LoadingCard;