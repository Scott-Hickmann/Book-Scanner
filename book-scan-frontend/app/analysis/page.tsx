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
      <HStack justifyContent="space-between" w="100%">
        <Heading size="2xl">Your Memories</Heading>
        <Button>Ask Questions</Button>
      </HStack>
      <Grid w="100%" templateColumns="repeat(2,1fr)" gap={6}>
        <GridItem id="summary" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Summary</Heading>
          <Text>This is a summary of the book</Text>
        </GridItem>
        <GridItem id="PDF" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">PDF</Heading>
          <Text>This is an analysis of the book</Text>
        </GridItem>
        <GridItem id="quote" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Quote</Heading>
          <Text>Uwu this is a quote</Text>
        </GridItem>
        <GridItem id="stats" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Stats</Heading>
        </GridItem>
      </Grid>
    </VStack>
  );
}
