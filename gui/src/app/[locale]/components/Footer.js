"use client";

import { useState } from "react";
import Link from "next/link";
import styles from "./Footer.module.css";
import { Language } from "@mui/icons-material";

export default function Footer() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen((prev) => !prev);
  };

  return (
    <footer className={styles.footer}>
      <div className={styles.languageSelector}>
        <button
          onClick={toggleMenu}
          className={styles.languageButton}
          aria-haspopup="menu"
          // aria-expanded={menuOpen}
        >
          <Language />
          Language
        </button>
        {menuOpen && (
          <div className={styles.menu} role="menu">
            <Link href="/en" className={styles.menuItem} role="menuitem">
              English
            </Link>
            <Link href="/de" className={styles.menuItem} role="menuitem">
              Deutsch
            </Link>
          </div>
        )}
      </div>
    </footer>
  );
}
