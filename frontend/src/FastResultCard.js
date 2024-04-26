import {
  Box,
  Divider,
  Heading,
  Text,
  useColorModeValue,
  VStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Link, useBreakpointValue,
} from "@chakra-ui/react";
import {Icon} from "@chakra-ui/icons";
import {FaBolt} from "react-icons/fa";
import React from "react";

const FastResultCard = ({ courses }) => {
  const borderColor = useColorModeValue("gray.300", "whiteAlpha.400");
  const bgColor = useColorModeValue("gray.100", "gray.700");
  const isMobile = useBreakpointValue({ base: true, md: false });

   const renderProfessorsTable = (professors) => { 
    const setNum = (x) => {
      if (x < 0) {
        return null
      } else {
        return x
      }
    }
    const parsedProfessors = professors;
    if (parsedProfessors === NaN|| parsedProfessors.join() === [].join()) {
      return (<><Box height="1rem" /><Text>Not Taught Fall 2024</Text></>);
    }
    if (parsedProfessors.join() === ["TBD"].join()) {
      return (<><Box height="1rem" /><Text>Course Offered Fall 2024 -- Professor TBD</Text></>);
    }
    return isMobile ? (
      <>
        <Box height="1rem" />
        {parsedProfessors.map((professor, index) => (
          <VStack key={index} align="start" spacing={1}>
            <Text fontWeight="bold">{professor.name || '-'}</Text>
            <Text>Instructor Quality: {setNum(professor.instructor_quality) || '-'}</Text>
            <Text>Course Quality: {setNum(professor.course_quality) || '-'}</Text>
            <Text>Difficulty: {setNum(professor.difficulty) || '-'}</Text>
            <Text>Work Required: {setNum(professor.work_required) || '-'}</Text>
          </VStack>
        ))}
      </>
    ) : (
        <>
        <Box height="1rem" />
      <Table variant="simple" size="sm">
        <Thead>
          <Tr>
            <Th>Instructor</Th>
            <Th>Instructor Quality</Th>
            <Th>Course Quality</Th>
            <Th>Difficulty</Th>
            <Th>Work Required</Th>
          </Tr>
        </Thead>
        <Tbody>
          {parsedProfessors.map((professor, index) => (
            <Tr key={index}>
              <Td>{professor.name || '-'}</Td>
              <Td>{setNum(professor.instructor_quality) || '-'}</Td>
              <Td>{setNum(professor.course_quality) || '-'}</Td>
              <Td>{setNum(professor.difficulty) || '-'}</Td>
              <Td>{setNum(professor.work_required) || '-'}</Td>
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
                  {course.department_code + course.course_code + ': ' + course.title}
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