import styles from "./Main.module.css";

export default function OtherInstances() {
  return (
    <div className={styles.otherInstances}>
      <div className={styles.ctas}>
        <a href="#" className={styles.secondary} target="_blank" rel="noopener noreferrer">
          Another instance?
        </a>
        <a href="#" className={styles.secondary} target="_blank" rel="noopener noreferrer">
          Another instance?
        </a>
      </div>
    </div>
  );
}
