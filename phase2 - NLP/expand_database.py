import pandas as pd

english_medicins= pd.read_csv('english_medicines.csv')
arabic_medicins=pd.read_csv('arabic_medicinces.csv')
arabicfreq=pd.read_csv('arabic_frequencies.csv')
englishfreq=pd.read_csv('english_frequencies.csv')

medicine_list=['Acetazolamide', 'Acetylcysteine', 'Albendazole', 'Amantadine', 'Amoxicillin', 'Artificial Tears', 'Atropine', 'Azithromycin', 'Bimatoprost', 'Botox', 'Brimonidine', 'Calcium Carbonate', 'Carbachol', 'Carbamazepine', 'Carbocisteine', 'Cefdinir', 'Cefixime', 'Cefuroxime', 'Cetirizine', 'Chloramphenicol', 'Chlorhexidine', 'Ciprofloxacin', 'Clindamycin', 'Collagen', 'Cyclosporine', 'Dexamethasone', 'Dextromethorphan', 'Diclofenac', 'Domperidone', 'Donepezil', 'Dorzolamide', 'Doxycycline', 'Erythromycin', 'Fluorometholone', 'Gabapentin', 'Gatifloxacin', 'Glycolic Acid', 'Guaifenesin', 'Hyaluronic Acid', 'Hydrocortisone', 'Hydroquinone', 'Hydroxyzine', 'Ibuprofen', 'Iron Supplements', 'Ketorolac', 'Lactic Acid', 'Latanoprost', 'Levetiracetam', 'Levofloxacin', 'Lidocaine', 'Lifitegrast', 'Loratadine', 'Mannitol', 'Mebendazole', 'Memantine', 'Metoclopramide', 'Metronidazole', 'Montelukast', 'Moxifloxacin', 'Multivitamins', 'Mupirocin', 'Natamycin', 'Nepafenac', 'Niacinamide', 'Nystatin', 'Ofloxacin', 'Omeprazole', 'Ondansetron', 'Oral Rehydration Salts', 'Paracetamol', 'Peptides', 'Pilocarpine', 'Pramipexole', 'Prednisolone', 'Prednisolone Acetate', 'Prednisolone Drops', 'Pregabalin', 'Probiotics', 'Ranitidine', 'Retinol', 'Rivastigmine', 'Ropinirole', 'Salbutamol', 'Salicylic Acid', 'Sodium Hyaluronate', 'Timolol', 'Tobramycin', 'Topiramate', 'Travoprost', 'Tretinoin', 'Tropicamide', 'Valproate', 'Vitamin C Serum', 'Vitamin D', 'Voriconazole', 'Zinc Sulfate', 'أتروبين', 'أزيثروميسين', 'أسيتات البريدنيزولون', 'أسيتازولاميد', 'أسيتيل سيستين', 'ألبيندازول', 'أمانتادين', 'أملاح الإماهة الفموية', 'أموكسيسيلين', 'أوفلوكساسين', 'أوميبرازول', 'أوندانسيترون', 'إريثرومايسين', 'إيبوبروفين', 'الببتيدات', 'البروبيوتيك', 'البوتوكس', 'الفيتامينات المتعددة', 'باراسيتامول', 'براميبيكسول', 'بريجابالين', 'بريدنيزولون', 'بريمونيدين', 'بيلوكاربين', 'بيماتوبروست', 'ترافوبروست', 'تروبيكاميد', 'تريتينوين', 'توبراميسين', 'توبيراميت', 'تيمولول', 'جابابنتين', 'جاتيفلوكساسين', 'حمض الجليكوليك', 'حمض الساليسيليك', 'حمض اللاكتيك', 'حمض الهيالورونيك', 'دموع صناعية', 'دورزولاميد', 'دوكسيسيكلين', 'دومبيريدون', 'دونيبيزيل', 'ديكساميثازون', 'ديكستروميثورفان', 'ديكلوفيناك', 'رانيتيدين', 'روبينيرول', 'ريتينول', 'ريفاستجمين', 'سالبيوتامول', 'سيبروفلوكساسين', 'سيتريزين', 'سيفدينير', 'سيفوريوكسيم', 'سيفيكسيم', 'سيكلوسبورين', 'غوايفينيسين', 'فالبروات', 'فلوروميثولون', 'فوريكونازول', 'فيتامين د', 'قطرات بريدنيزولون', 'كارباشول', 'كاربامازيبين', 'كاربوسيستين', 'كبريتات الزنك', 'كربونات الكالسيوم', 'كلورامفينيكول', 'كلورهيكسيدين', 'كليندامايسين', 'كولاجين', 'كيتورولاك', 'لاتانوبروست', 'لوراتادين', 'ليدوكايين', 'ليفوفلوكساسين', 'ليفيتيجراست', 'ليفيتيراسيتام', 'مانيتول', 'مصل فيتامين سي', 'مكملات الحديد', 'موبيروسين', 'موكسيفلوكساسين', 'مونتيلوكاست', 'ميبيندازول', 'ميترونيدازول', 'ميتوكلوبراميد', 'ميمانتين', 'ناتاميسين', 'نياسيناميد', 'نيبافيناك', 'نيستاتين', 'هيالورونات الصوديوم', 'هيدروكسيزين', 'هيدروكورتيزون', 'هيدروكينون']

# dol bto3na
df_medicines_e = english_medicins['medicine'].tolist()
df_medicines_a = arabic_medicins['medicine'].tolist()
arabicfreq = arabicfreq['frequency'].tolist()
englishfreq = englishfreq['frequency'].tolist()
# dol bto3hom
ArabicWords=['٨', 'دقائق', '١٢', 'قبل', 'الأكل', 'أسبوع', '٥', 'النوم', 'ليلا', 'ساعات', 'لأول', 'يوم', 'مرة', 'اليقظة', '٤', 'كل', '٧', 'دقيقة', 'أثناء', '٣', '٦', 'يومين', 'الفطار', 'مرتين', '١٤', 'واحدة', 'أيام', 'الغداء', 'اللزوم', 'ساعة', 'لمدة', 'يوميا', 'بعد', 'فقط', 'صباحا', 'عند', '١٥' ,'أتروبين', 'أزيثروميسين', 'أسيتات البريدنيزولون', 'أسيتازولاميد', 'أسيتيل سيستين', 'ألبيندازول', 'أمانتادين', 'أملاح الإماهة الفموية', 'أموكسيسيلين', 'أوفلوكساسين', 'أوميبرازول', 'أوندانسيترون', 'إريثرومايسين', 'إيبوبروفين', 'الببتيدات', 'البروبيوتيك', 'البوتوكس', 'الفيتامينات المتعددة', 'باراسيتامول', 'براميبيكسول', 'بريجابالين', 'بريدنيزولون', 'بريمونيدين', 'بيلوكاربين', 'بيماتوبروست', 'ترافوبروست', 'تروبيكاميد', 'تريتينوين', 'توبراميسين', 'توبيراميت', 'تيمولول', 'جابابنتين', 'جاتيفلوكساسين', 'حمض الجليكوليك', 'حمض الساليسيليك', 'حمض اللاكتيك', 'حمض الهيالورونيك', 'دموع صناعية', 'دورزولاميد', 'دوكسيسيكلين', 'دومبيريدون', 'دونيبيزيل', 'ديكساميثازون', 'ديكستروميثورفان', 'ديكلوفيناك', 'رانيتيدين', 'روبينيرول', 'ريتينول', 'ريفاستجمين', 'سالبيوتامول', 'سيبروفلوكساسين', 'سيتريزين', 'سيفدينير', 'سيفوريوكسيم', 'سيفيكسيم', 'سيكلوسبورين', 'غوايفينيسين', 'فالبروات', 'فلوروميثولون', 'فوريكونازول', 'فيتامين د', 'قطرات بريدنيزولون', 'كارباشول', 'كاربامازيبين', 'كاربوسيستين', 'كبريتات الزنك', 'كربونات الكالسيوم', 'كلورامفينيكول', 'كلورهيكسيدين', 'كليندامايسين', 'كولاجين', 'كيتورولاك', 'لاتانوبروست', 'لوراتادين', 'ليدوكايين', 'ليفوفلوكساسين', 'ليفيتيجراست', 'ليفيتيراسيتام', 'مانيتول', 'مصل فيتامين سي', 'مكملات الحديد', 'موبيروسين', 'موكسيفلوكساسين', 'مونتيلوكاست', 'ميبيندازول', 'ميترونيدازول', 'ميتوكلوبراميد', 'ميمانتين', 'ناتاميسين', 'نياسيناميد', 'نيبافيناك', 'نيستاتين', 'هيالورونات الصوديوم', 'هيدروكسيزين', 'هيدروكورتيزون', 'هيدروكينون']
EnglishWords=['Acetazolamide', 'Acetylcysteine', 'Albendazole', 'Amantadine', 'Amoxicillin', 'Artificial Tears', 'Atropine', 'Azithromycin', 'Bimatoprost', 'Botox', 'Brimonidine', 'Calcium Carbonate', 'Carbachol', 'Carbamazepine', 'Carbocisteine', 'Cefdinir', 'Cefixime', 'Cefuroxime', 'Cetirizine', 'Chloramphenicol', 'Chlorhexidine', 'Ciprofloxacin', 'Clindamycin', 'Collagen', 'Cyclosporine', 'Dexamethasone', 'Dextromethorphan', 'Diclofenac', 'Domperidone', 'Donepezil', 'Dorzolamide', 'Doxycycline', 'Erythromycin', 'Fluorometholone', 'Gabapentin', 'Gatifloxacin', 'Glycolic Acid', 'Guaifenesin', 'Hyaluronic Acid', 'Hydrocortisone', 'Hydroquinone', 'Hydroxyzine', 'Ibuprofen', 'Iron Supplements', 'Ketorolac', 'Lactic Acid', 'Latanoprost', 'Levetiracetam', 'Levofloxacin', 'Lidocaine', 'Lifitegrast', 'Loratadine', 'Mannitol', 'Mebendazole', 'Memantine', 'Metoclopramide', 'Metronidazole', 'Montelukast', 'Moxifloxacin', 'Multivitamins', 'Mupirocin', 'Natamycin', 'Nepafenac', 'Niacinamide', 'Nystatin', 'Ofloxacin', 'Omeprazole', 'Ondansetron', 'Oral Rehydration Salts', 'Paracetamol', 'Peptides', 'Pilocarpine', 'Pramipexole', 'Prednisolone', 'Prednisolone Acetate', 'Prednisolone Drops', 'Pregabalin', 'Probiotics', 'Ranitidine', 'Retinol', 'Rivastigmine', 'Ropinirole', 'Salbutamol', 'Salicylic Acid', 'Sodium Hyaluronate', 'Timolol', 'Tobramycin', 'Topiramate', 'Travoprost', 'Tretinoin', 'Tropicamide', 'Valproate', 'Vitamin C Serum', 'Vitamin D', 'Voriconazole', 'Zinc Sulfate''for', 'Every', 'After', 'Twice', 'needed', 'first', 'hours', 'breakfast', 'For', '8', 'awake', 'other', 'Night', 'hour', 'Morning', 'bed', '14', 'the', 'days', 'As', '5', 'bedtime', 'lunch', 'week', '7', 'daily', 'only', '4', 'Before', 'while', '3', 'minutes', '2', '6', 'day', '15', 'meals', 'Once', '12']

df_medicines_a = [med.lower() for med in df_medicines_a]
df_medicines_e = [med.lower() for med in df_medicines_e]
medicine_list = [med.lower() for med in medicine_list]
arabicfreq = [freq.lower() for freq in arabicfreq]
englishfreq = [freq.lower() for freq in englishfreq]
EnglishWords = [freq.lower() for freq in EnglishWords]
ArabicWords = [freq.lower() for freq in ArabicWords]

# Combine both lists
all_medicines_lower = df_medicines_e + df_medicines_a
all_medicines_lower = pd.unique(all_medicines_lower).tolist()
medicine_list.extend(all_medicines_lower)

# list of all words
EnglishWords += (df_medicines_e+ englishfreq)
ArabicWords += (df_medicines_a+arabicfreq)

ArabicWords = pd.unique(ArabicWords).tolist()
EnglishWords = pd.unique(EnglishWords).tolist()
medicine_list = pd.unique(medicine_list).tolist()

ArabicWords
EnglishWords
medicine_list

