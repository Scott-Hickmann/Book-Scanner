// app/page.tsx
"use client";

import { Heading, VStack, Text, Box, Button, Icon } from "@chakra-ui/react";

import { ArrowForwardIcon } from "@chakra-ui/icons";
import DocStream from "./components/docStream";

export default function Page() {
  return (
    <VStack h="100%" >
      <VStack p={5} borderBottom="1px" borderColor="gray.200" h="100%">
        <Heading size="3xl">Recollect</Heading>
        <Text fontSize="xl">Your Memories, Preserved Forever</Text>
      </VStack>
      <DocStream/>
    </VStack>
  );
}
