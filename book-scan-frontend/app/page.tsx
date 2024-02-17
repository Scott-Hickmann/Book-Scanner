// app/page.tsx
"use client";

import { Heading, VStack, Text, Box, Button, Icon } from "@chakra-ui/react";
import Lottie from "lottie-react";
import bookFlipAnimation from "../public/book-flip.json";
import { ArrowForwardIcon } from "@chakra-ui/icons";

export default function Page() {
  return (
    <VStack h="100%">
      <VStack p={5} borderBottom="1px" borderColor="gray.200" >
        <Heading size="3xl">Recollect</Heading>
        <Text fontSize="xl">Your Memories, Preserved Forever</Text>
      </VStack>
      <Box id="lottie" maxW="xl" maxH="xl">
        <Lottie animationData={bookFlipAnimation} loop={true} />
      </Box>
      <Button>
        Start Scanning <Icon as={ArrowForwardIcon} ml={2} />
      </Button>
    </VStack>
  );
}
