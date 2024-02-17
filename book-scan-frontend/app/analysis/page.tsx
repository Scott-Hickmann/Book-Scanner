// app/page.tsx
"use client";

import {
  Box,
  Button,
  Grid,
  GridItem,
  HStack,
  Heading,
  Text,
  VStack,
} from "@chakra-ui/react";

export default function Page() {
  return (
    <VStack w={{ base: "100%", md: "50%" }} margin="auto" p={3}>
      <HStack
        justifyContent="space-between"
        w="100%"
        borderBottom="1px"
        borderColor="gray.600"
        p={3}
        mb={5}
      >
        <Heading size="2xl">Your Memories</Heading>
        <Button>Ask Questions</Button>
      </HStack>
      <Heading>No document has been scanned!</Heading>
    </VStack>
  );
}
