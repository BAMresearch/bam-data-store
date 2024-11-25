import styles from "./Main.module.css";

export default function MainButtons() {
  return (
    <div className={styles.hrefsButtons}>
      <div className={styles.ctas}>
        <a href="https://main.datastore.bam.de/" className={styles.primary} target="_blank" rel="noopener noreferrer">
          Main instance of the Data Store
        </a>
        <a href="https://datastore.bam.de/en/home" className={styles.primary} target="_blank" rel="noopener noreferrer">
          Documentation
        </a>
        <a href="#" className={styles.primary} target="_blank" rel="noopener noreferrer">
          Masterdata Tools
        </a>
      </div>
    </div>
  );
}
