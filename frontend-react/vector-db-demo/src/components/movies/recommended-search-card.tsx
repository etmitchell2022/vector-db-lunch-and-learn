import React from "react";
import { Badge } from "../ui/badge";
import { cn } from "@/lib/utils";

type RecommendedSearchCardProps = {
  className?: string;
  searchValue: string;
  onClick?: () => void;
};

const RecommendedSearchCard: React.FC<RecommendedSearchCardProps> = ({
  className,
  searchValue,
  onClick,
}) => {
  return (
    <Badge
      variant="outline"
      className={cn(
        "px-3 py-2 cursor-pointer hover:border-gray-300 ",
        className
      )}
      onClick={onClick}
    >
      {searchValue}
    </Badge>
  );
};

export default RecommendedSearchCard;
