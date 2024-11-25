import styles from "./Main.module.css";
import Welcome from "./Welcome";
import MainButtons from "./MainButtons";
import OtherInstances from "./OtherInstances";

export default function Main() {
  return (
    <main className={styles.main}>
      <Welcome />
      <MainButtons />
      <OtherInstances />
    </main>
  );
}
