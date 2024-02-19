"use client";

import {
  Heading,
  VStack,
  Text,
  Box,
  Button,
  Icon,
  Link,
  HStack,
  useColorMode,
  IconButton,
  Spacer,
} from "@chakra-ui/react";
import { SunIcon } from "@chakra-ui/icons";
import DocStream from "./components/docStream";

export default function Page() {
  const { toggleColorMode } = useColorMode();

  return (
    <VStack h="100%" minH="100vh" justifyContent="space-between" w="100%">
      <HStack w="100%" borderBottom="1px" borderColor="gray.600" px={8}>
        <Button as={Link} isDisabled>
          Past Scans
        </Button>
        <VStack p={5} h="100%" w="100%">
          <Heading size="3xl">Recollect</Heading>
          <Text fontSize="xl">Your Memories, Preserved Forever</Text>
        </VStack>
        <IconButton
          aria-label="Darkmode"
          icon={<SunIcon />}
          onClick={toggleColorMode}
        />
      </HStack>
      <Box h="100%">
        <DocStream />
      </Box>
      <Spacer/>
      <Text py={5} color="darkgray">Made with 💚 by Lawton, Scott, Kaien, Jason</Text>
    </VStack>
  );
}
