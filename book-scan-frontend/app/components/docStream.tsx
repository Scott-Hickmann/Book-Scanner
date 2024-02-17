import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { Box, Image, VStack, Text, Button } from "@chakra-ui/react";
import Lottie from "lottie-react";
import bookFlipAnimation from "../../public/book-flip.json";
import Link from "next/link";
import { get } from "http";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function DocStream() {
  const [imageUrl, setImageUrl] = useState<string>("");
  const [docId, setDocId] = useState<string>("");

  useEffect(() => {
    // Function to fetch and set the image URL
    const fetchAndSetImageUrl = async (imageName: string) => {
      const { data, error } = await supabase.storage
        .from("public/images")
        .download(imageName);

      if (error) {
        console.error("Error fetching image:", error);
        return;
      }

      const url = URL.createObjectURL(data);
      setImageUrl(url);
    };

    // Set up a real-time subscription to the 'images' table

    const img_subscription = supabase
      .channel("images-updates-watcher")
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "images" },
        async (payload) => {
          console.log("Change received!", payload);
          await fetchAndSetImageUrl(payload.new.image_name);
          await setDocId(payload.new.doc_id);
        }
      )
      .subscribe();

    // Cleanup function to remove the subscription
    return () => {
      supabase.removeChannel(img_subscription);
    };
  }, []); // Empty dependency array to run only once on mount

  console.log(docId);
  return (
    <VStack maxH="50%">
      <Box>
        {/* {imageUrl ? ( */}
          <>
            <Box pos="relative">
              <Image src={imageUrl} alt="Document" />
            </Box>
            <Button
              as={Link}
              href={`/analysis/${docId}`}
              colorScheme="teal"
              size="lg"
            >
              Analyze PDF
            </Button>
          </>
        {/* ) : (
          <VStack id="lottie" maxW="xl" maxH="xl">
            <Lottie animationData={bookFlipAnimation} loop={true} />
            <Text fontStyle="italic">Waiting for your scan...</Text>
          </VStack>
        )} */}
      </Box>
    </VStack>
  );
}
