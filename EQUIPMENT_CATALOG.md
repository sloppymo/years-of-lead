# Years of Lead - Complete Equipment Catalog

## 📋 **Equipment Overview**

This catalog lists all available equipment in Years of Lead, organized by category with detailed specifications including concealment ratings, legal status, and special properties.

---

## 🔫 **WEAPONS**

### Compact Pistol
- **Item ID**: `wpn_001`
- **Name**: Compact Pistol
- **Category**: Weapon
- **Concealment Rating**: 0.7 (70% concealable)
- **Container Bonus**: +0.1 (additional concealment in containers)
- **Legal Status**: RESTRICTED (requires permit)
- **Weight**: 1.2 kg
- **Bulk**: 0.8
- **Description**: Small, easily concealed handgun
- **Special Properties**:
  - Unregistered Serial Number flag
  - Smuggled flag
  - Uniform-specific consequences (confiscation for uniformed personnel)

---

## 📱 **ELECTRONICS**

### Encrypted Communication Device
- **Item ID**: `elc_001`
- **Name**: Encrypted Communication Device
- **Category**: Electronic
- **Concealment Rating**: 0.8 (80% concealable)
- **Container Bonus**: +0.2 (significant bonus in containers)
- **Legal Status**: PROHIBITED (illegal to possess)
- **Description**: Military-grade encrypted communicator
- **Special Properties**:
  - Military Encryption flag
  - Foreign Made flag

---

## 📄 **DOCUMENTS**

### Forged Identification Papers
- **Item ID**: `doc_001`
- **Name**: Forged Identification Papers
- **Category**: Document
- **Concealment Rating**: 0.9 (90% concealable)
- **Container Bonus**: +0.05 (minimal bonus)
- **Legal Status**: CONTRABAND (extremely illegal)
- **Description**: High-quality forged identification documents
- **Special Properties**:
  - Professional Forgery flag
  - Government Seal flag

---

## 🏥 **MEDICAL**

### Field Medical Kit
- **Item ID**: `med_001`
- **Name**: Field Medical Kit
- **Category**: Medical
- **Concealment Rating**: 0.2 (20% concealable - very difficult to hide)
- **Concealable**: False
- **Legal Status**: LEGAL
- **Description**: Professional medical supplies

---

## 🏷️ **EQUIPMENT FLAGS**

### Unregistered Serial Number
- **Flag ID**: `unregistered_serial`
- **Description**: Item has filed-off or altered serial number
- **Concealment Modifier**: 0.0 (no effect on concealment)
- **Suspicion Modifier**: +0.3 (increases suspicion if detected)

### Smuggled Item
- **Flag ID**: `smuggled`
- **Description**: Item was illegally imported
- **Concealment Modifier**: -0.1 (slightly harder to conceal)
- **Suspicion Modifier**: +0.2 (increases suspicion if detected)

### Military Encryption
- **Flag ID**: `military_encryption`
- **Description**: Uses military-grade encryption protocols
- **Concealment Modifier**: +0.1 (slightly easier to conceal)
- **Suspicion Modifier**: +0.4 (significantly increases suspicion)

### Professional Forgery
- **Flag ID**: `professional_forgery`
- **Description**: High-quality forged document
- **Concealment Modifier**: +0.2 (easier to conceal)
- **Suspicion Modifier**: -0.1 (slightly reduces suspicion)

---

## 📊 **EQUIPMENT CATEGORIES**

### Available Categories:
1. **Weapon** - Firearms and melee weapons
2. **Armor** - Protective equipment
3. **Electronic** - Communication and computing devices
4. **Medical** - Health and medical supplies
5. **Document** - Papers, IDs, and written materials
6. **Tool** - General tools and equipment
7. **Contraband** - Illegal items
8. **Currency** - Money and valuables
9. **Communication** - Communication devices
10. **Explosive** - Explosives and explosive devices

---

## ⚖️ **LEGAL STATUS SYSTEM**

### Legal Status Levels:
- **LEGAL**: Completely legal to possess
- **RESTRICTED**: Legal with proper permits/licenses
- **PROHIBITED**: Illegal to possess
- **CONTRABAND**: Extremely illegal, severe consequences

---

## 🔍 **CONCEALMENT MECHANICS**

### Concealment Ratings:
- **0.0-0.3**: Very difficult to conceal (medical kits, large items)
- **0.4-0.6**: Moderately concealable (standard items)
- **0.7-0.8**: Easily concealable (small weapons, electronics)
- **0.9-1.0**: Highly concealable (documents, small items)

### Container Bonuses:
- Items in containers receive additional concealment bonuses
- Different item types have different container effectiveness

---

## 🎭 **SEARCH ENCOUNTER SYSTEM**

### Uniform Types Affecting Searches:
- **Civilian** - No special treatment
- **Medical** - Medical personnel uniform
- **Maintenance** - Maintenance worker uniform
- **Delivery** - Delivery personnel uniform
- **Press** - Press/media uniform
- **Official** - Government official uniform
- **Security** - Security personnel uniform

### Consequence Types:
- **Ignore** - No action taken
- **Confiscate and Warn** - Item taken, warning issued
- **Confiscate and Fine** - Item taken, fine imposed
- **Interrogation and Confiscation** - Questioning and item seizure
- **Arrest** - Immediate arrest
- **Arrest and Flag** - Arrest with additional flagging
- **Immediate Detention** - Extended detention
- **Mild Suspicion Only** - Minor suspicion noted
- **Item Logged but Released** - Item recorded but returned

---

## 📈 **SYSTEM STATISTICS**

- **Total Equipment Items**: 4 (currently implemented)
- **Equipment Categories**: 10 (defined)
- **Equipment Flags**: 4 (implemented)
- **Legal Status Types**: 4
- **Uniform Types**: 7
- **Consequence Types**: 9

---

## 🔧 **CUSTOMIZATION**

The equipment system supports custom equipment creation through the `create_custom_equipment()` function, allowing for:
- Custom item IDs and names
- Category assignment
- Concealment and legal status configuration
- Flag association
- Weight, bulk, and value specification

---

*This catalog represents the current state of equipment in Years of Lead as of the latest implementation. New equipment can be added through the equipment system's registration functions.* 