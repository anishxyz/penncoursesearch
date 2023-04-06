import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Text,
  VStack,
  Box,
  UnorderedList,
  ListItem
} from "@chakra-ui/react";

const InfoModal = ({ isOpen, onClose }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay style={{ backdropFilter: "blur(2px)", backgroundColor: "rgba(0, 0, 0, 0.2)" }} />
      <ModalContent>
        <ModalHeader>Welcome to Penn Course Search</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack align="start" spacing={4}>
            <Text>
              Penn Course Search is a search engine for the entire UPenn
              course catalog. It is built to help you truly find courses based
              on interests, career paths, or sheer curiosity.
            </Text>
            <Text fontWeight="bold">Examples:</Text>
            <VStack align="start" spacing={1}>
              <Text> - Recommend some courses to learn web development</Text>
              <Text> - Suggest some classes to take to learn about war</Text>
              <Text> - I’m interested in learning about law — give me some introductory
                classes
              </Text>
            </VStack>
            <Text>
              Please note: It is still in beta so some results might not be 100%
              accurate.
            </Text>
          </VStack>
          <Box alignSelf="flex-start" mt={4}>
            <Text>- Anish</Text>
          </Box>
        </ModalBody>
        <ModalFooter>
          <Button colorScheme="orange" onClick={onClose}>
            Close
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default InfoModal;
