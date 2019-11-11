from scraper import login, search_jobs, scrape_links, scrape_job_description
from time import sleep
from textacy import make_spacy_doc
from textacy.corpus import Corpus

FILEPATH = 'data/corpus'

def prepare_corpus(file=FILEPATH, lang='en'):
    # Load the corpus if it exists, create one if it doesn't
    try:
        c = Corpus.load(lang, filepath=file)
    except OSError:
        c = Corpus(lang)
    return c


if __name__ == '__main__':

    corpus = prepare_corpus()
    login()
    link = search_jobs('Data Analyst', 'Los Angeles, California')
    job_links = scrape_links(link, num_pages=40)
    print(len(job_links))
    i = 0


    for j in job_links:
        sleep(3)

        i += 1; print(i)
        job = scrape_job_description(j)
        record = (str(job.description), {
            'title': job.title,
            'location': job.location,
            'experience_level': job.experience_level,
            'industries': job.industries,
            'employment_type': job.employment_type,
            'job_functions': job.job_functions,
            'company': job.company,
            'job_id': job.job_id,
            'url': job.url
        })

        doc = make_spacy_doc(record, lang='en')
        corpus.add_doc(doc)

    corpus.save(FILEPATH)

