"use client";

import { axiosClient } from "@/api/axios-client";
import { usePostApiV1MoviesSearch } from "@/api/generated/movies/movies";
import RecommendedSearchCard from "@/components/movies/recommended-search-card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ArrowRightIcon } from "lucide-react";
import { useEffect, useState } from "react";

const mockMovieSearches = [
  "Intense action with lots of explosions and car chases",
  "A movie about the future",
  "Underdog sports team overcoming impossible odds",
  "Comedy about a group of friends",
];

export default function Movies() {
  const [searchValue, setSearchValue] = useState("");

  const { mutate, isLoading, data, error } = usePostApiV1MoviesSearch();

  const handleSearch = () => {
    if (!searchValue) return;
    mutate({ data: { search: searchValue } });
  };

  useEffect(() => {
    console.log("data", data);
  }, [data]);
  return (
    <div className="flex flex-col min-h-screen">
      {/* <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"></header> */}

      <main className="flex-1 container py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          <div className="text-center space-y-2">
            <h1 className="text-4xl font-bold">Vector Movie Search</h1>
          </div>
          <div className="text-center space-y-4"></div>

          {/* Search Interface */}
          <div className="relative bg-[#fafafa] flex h-40  rounded-xl border-gray-900 border-t-0 border-b-0">
            <Textarea
              className="h-full resize-none text-black/80 placeholder:text-black/60 rounded-xl"
              placeholder="Describe the movie you want to watch..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
            <Button
              size="icon"
              className="rounded-full absolute bottom-3 right-3 cursor-pointer"
              onClick={handleSearch}
            >
              <ArrowRightIcon className="h-6 w-6" />
            </Button>
          </div>

          {/* Recommended Prompts */}
          <div className="flex flex-row items-center justify-evenly flex-wrap h-6 gap-y-2">
            {mockMovieSearches.map((search, index) => (
              <RecommendedSearchCard
                key={index}
                searchValue={search}
                onClick={() => setSearchValue(search)}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
