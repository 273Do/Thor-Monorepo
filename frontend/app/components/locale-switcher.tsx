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
  const { t, i18n } = useTranslation();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button size="icon" variant="outline">
          <Languages />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuGroup>
          <DropdownMenuLabel>{t("language.title")}</DropdownMenuLabel>
          <DropdownMenuRadioGroup
            value={i18n.language}
            onValueChange={(lang) => i18n.changeLanguage(lang)}
          >
            <DropdownMenuRadioItem value="ja">
              {t("language.ja")}
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="en">
              {t("language.en")}
            </DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
