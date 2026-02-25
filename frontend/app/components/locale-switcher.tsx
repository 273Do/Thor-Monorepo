import { useTranslation } from "react-i18next";

import { Languages } from "lucide-react";

import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

export const LocaleSwitcher = () => {
  const { i18n } = useTranslation();

  console.log(i18n.language);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button size="icon" variant="outline">
          <Languages />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuGroup>
          <DropdownMenuLabel>Language</DropdownMenuLabel>
          <DropdownMenuRadioGroup
            value={i18n.language}
            onValueChange={(lang) => i18n.changeLanguage(lang)}
          >
            <DropdownMenuRadioItem value="ja">日本語</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="en">English</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
