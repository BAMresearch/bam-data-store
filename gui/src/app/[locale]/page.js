import styles from "./page.module.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Main  from "./components/Main";

/**
 * Home page. This is divided into 3 main components: Header, Main and Footer.
 * @returns
 */
export default function Home() {
  return (
    <div className={styles.page}>
      <Header />
      <Main />
      <Footer />
    </div>
  );
}
