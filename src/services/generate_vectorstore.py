from src.storage.datasets import Datasets
from src.storage.vectorstore import Vectorstore

# Gather documents
raw_docs = []

profile = Datasets.get_profile()
raw_docs.append(profile)

katalog_df = Datasets.get_catalog()
for _, item in katalog_df.iterrows():
    doc = str(item['Nama Produk'])
    doc += f"\n{str(item['Deskripsi'])}"
    doc += f"\nKeunggulan: {str(item['Keunggulan'])}"
    doc += f"\nKategori: {str(item['Kategori'])}"

    price = format(int(item['Harga (Rp)']), ',').replace(',', '.')
    doc += f"\nHarga: Rp{price}"

    raw_docs.append(doc)

faq_df = Datasets.get_faq()
for _, qna in faq_df.iterrows():
    doc = f"\nPertanyaan: {str(qna['Pertanyaan'])}"
    doc += f"\nJawaban: {str(qna['Jawaban'])}"
    raw_docs.append(doc)

# Save vector store
vectorstore = Vectorstore()
vectorstore.save_vectorstore(raw_docs=raw_docs)