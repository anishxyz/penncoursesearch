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
  Link,
  Kbd
} from "@chakra-ui/react";

const InfoModal = ({ isOpen, onClose }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay style={{ backdropFilter: "blur(2px)", backgroundColor: "rgba(0, 0, 0, 0.2)" }} />
      <ModalContent>
        <ModalHeader>Introducing Penn Course Search 🎉</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack align="start" spacing={4}>
            <Text>
              The first AI powered search engine for the UPenn course catalog.
            </Text>
            <Text>
              With Penn Course Search, students can search for courses based on interests, topics, career paths and more!
            </Text>
            <Text fontWeight="bold">Examples:</Text>
            <VStack align="start" spacing={1}>
              <Text> - "I want to learn about typography"</Text>
              <Text> - "Teach me about product design"</Text>
              <Text> - "Compare and contrast CIS 2400 and ESE 3500"</Text>
              <Text> - "I want to become a VC"</Text>
            </VStack>
            <Text>
              Press <Kbd>m</Kbd> to toggle light/dark mode.
            </Text>
            <Text color="red.500">
              Please note: It is still in beta so some results might not be 100% accurate.
            </Text>
            <Link href="https://forms.gle/5tpjCZ1xZjbCuAwL6" isExternal color="orange.500">
              <Text>
                Feedback form
              </Text>
            </Link>
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
