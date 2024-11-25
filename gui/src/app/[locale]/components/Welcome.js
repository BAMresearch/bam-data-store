import styles from "./Main.module.css";

export default function Welcome() {
  return (
    <div className={`${styles.welcome} ${styles.main}`}>
      <h1 className={styles.title}>Welcome to BAM Data Store website!</h1>
      <ol>
        <li>
          Get started by editing <code>app/page.js</code>.
        </li>
        <li>Save and see your changes instantly.</li>
      </ol>
    </div>
  );
}
