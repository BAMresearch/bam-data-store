"use client";

import Image from "next/image";
import styles from "./Header.module.css";
import {useTheme} from "./context/ThemeContext"
import { LightMode, DarkMode } from "@mui/icons-material";


export default function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className={styles.header}>
      <div className={styles.logoBox}>
        <Image
          src="/DataStore_Project_WithLabel.svg"
          alt="DataStore Logo with text"
          width={50}
          height={50}
          className={styles.logo}
        />
      </div>
      <div className={styles.contactBox}>
        <a href="#" className={styles.contact}>Contact</a>
      </div>
      <button onClick={toggleTheme} className={styles.themeToggle}>
        {theme === "light" ? <LightMode />: <DarkMode />}
      </button>
    </header>
  );
}
