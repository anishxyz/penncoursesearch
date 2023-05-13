import {Box, Divider, Heading, Text, useColorModeValue, VStack, Table, Thead, Tbody, Tr, Th, Td, Link} from "@chakra-ui/react";
import {Icon} from "@chakra-ui/icons";
import {FaBolt} from "react-icons/fa";
import React from "react";
import { useMediaQuery } from '@chakra-ui/react';

const FastResultCard = ({ courses }) => {
  const borderColor = useColorModeValue("gray.300", "whiteAlpha.400");
  const bgColor = useColorModeValue("gray.100", "gray.700");

  const renderProfessorsTable = (professors) => {
    const parsedProfessors = JSON.parse(professors);

    if (parsedProfessors.join() === [].join()) {
      return (<><Box height="1rem" /><Text>Not Taught Fall 2023</Text></>);
    }
    if (parsedProfessors.join() === ["TBD"].join()) {
      return (<><Box height="1rem" /><Text>Course Offered Fall 2023 -- Professor TBD</Text></>);
    }
    return (
    <>
      <Box height="1rem" /> {/* Add spacer */}
      <Table variant="simple" size="sm">
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Course Quality</Th>
            <Th>Difficulty</Th>
            <Th>Instructor Quality</Th>
            <Th>Work Required</Th>
          </Tr>
        </Thead>
        <Tbody>
          {parsedProfessors.map((professor, index) => (
            <Tr key={index}>
              <Td>{professor.name}</Td>
              <Td>{professor.course_quality}</Td>
              <Td>{professor.difficulty}</Td>
              <Td>{professor.instructor_quality}</Td>
              <Td>{professor.work_required}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </>
  );
  }

  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      overflowY="scroll"
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
                <Link href={course.link}>
                  {course.id.replace("-", " ") + ': ' + course.title}
                </Link>
              </Heading>
              <Text style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
                {course.description}
              </Text>
              {renderProfessorsTable(course.professor_stats)}
            </Box>
          </React.Fragment>
        ))}
      </VStack>
    </Box>
  );
};

export default FastResultCard;