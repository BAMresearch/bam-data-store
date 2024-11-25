import styles from "./Main.module.css";
import { useTranslations } from 'next-intl';


export default function MainButtons( ) {
  const t = useTranslations("MainButtons");

  return (
    <div className={styles.hrefsButtons}>
      <div className={styles.ctas}>
        <a href="https://main.datastore.bam.de/" className={styles.primary} target="_blank" rel="noopener noreferrer">
          {t('mainInstance')}
        </a>
        <a href="https://datastore.bam.de/en/home" className={styles.primary} target="_blank" rel="noopener noreferrer">
          {t('wiki')}
        </a>
        <a href="/en" className={styles.primary} target="_blank" rel="noopener noreferrer">
          {t('masterdataTools')}
        </a>
      </div>
    </div>
  );
}
