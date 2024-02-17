import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { Box, Image, VStack } from "@chakra-ui/react";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function DocStream() {
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    const fetchImage = async () => {
      const { data, error } = await supabase.storage
        .from("public/images")
        .download("uwu.jpeg");

      if (error) {
        console.error("Error fetching image:", error);
        return;
      }

      const url = URL.createObjectURL(data);
      setImageUrl(url);
      console.log("Image URL:", url);
    };

    fetchImage();
  }, []); // Empty dependency array to run only once on mount

  return (
    <VStack maxH="50%">
      <h1>Imagestream of docs should be below</h1>
      <Box>
      {imageUrl && <Image src={imageUrl} alt="Document" />}
      </Box>
    </VStack>
  );
}
