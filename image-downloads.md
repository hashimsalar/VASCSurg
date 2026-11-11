# Images to download

These are the Wikimedia Commons images the site still needs. Wikimedia throttles the cloud machine that builds the site, so they have to be downloaded from a normal computer.

## How to do it

1. Open each link below and save the image (right-click, **Save image as**). Keep the file name the browser suggests; don't rename it.
2. Upload the saved files to `assets/img/` on the branch `claude/inspiring-clarke-x9d5cw`. On GitHub: switch to that branch, open the `assets/img` folder, choose **Add file > Upload files**, drag the files in, and commit directly to the branch.
3. Tell Claude. It runs `python3 scripts/fetch_images.py --from assets/img`, which matches each file to its figure, looks up the author and license on Wikimedia, resizes it to WebP, places it in the page with its credit line, and then removes the uploaded originals.

Partial batches are fine: anything not in the folder yet is skipped and can be added later.

## The 60 files


### Foundations

1. [Right proximal common carotid artery normal spectral flow.jpg](https://upload.wikimedia.org/wikipedia/commons/0/01/Right_proximal_common_carotid_artery_normal_spectral_flow.jpg) (figure: carotid-spectral-doppler; [Commons page](https://commons.wikimedia.org/wiki/File:Right_proximal_common_carotid_artery_normal_spectral_flow.jpg))
2. [Volume rendered CT scan of abdominal and pelvic blood vessels (smaller).gif](https://upload.wikimedia.org/wikipedia/commons/c/c5/Volume_rendered_CT_scan_of_abdominal_and_pelvic_blood_vessels_%28smaller%29.gif) (figure: cta-volume-rendered; [Commons page](https://commons.wikimedia.org/wiki/File:Volume_rendered_CT_scan_of_abdominal_and_pelvic_blood_vessels_(smaller).gif))
3. [Coagulation full.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b6/Coagulation_full.svg/1920px-Coagulation_full.svg.png) (figure: coagulation-cascade; [Commons page](https://commons.wikimedia.org/wiki/File:Coagulation_full.svg))
4. [Late complications of atherosclerosis.PNG](https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5b/Late_complications_of_atherosclerosis.PNG/1920px-Late_complications_of_atherosclerosis.PNG) (figure: atherosclerosis-complications; [Commons page](https://commons.wikimedia.org/wiki/File:Late_complications_of_atherosclerosis.PNG))
5. [Normal 12 lead EKG.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/1/18/Normal_12_lead_EKG.jpg/1920px-Normal_12_lead_EKG.jpg) (figure: ecg-12-lead; [Commons page](https://commons.wikimedia.org/wiki/File:Normal_12_lead_EKG.jpg))

### Presentations

6. [Blausen Peripheral Arterial Disease eng.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/7/70/Blausen_Peripheral_Arterial_Disease_eng.svg/1920px-Blausen_Peripheral_Arterial_Disease_eng.svg.png) (figure: pad-illustration; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_Peripheral_Arterial_Disease_eng.svg))
7. [Arterial ulcer peripheral vascular disease.jpg](https://upload.wikimedia.org/wikipedia/commons/3/30/Arterial_ulcer_peripheral_vascular_disease.jpg) (figure: arterial-ulcer; [Commons page](https://commons.wikimedia.org/wiki/File:Arterial_ulcer_peripheral_vascular_disease.jpg))
8. [Arterial thrombosis causing cyanosis.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4f/Arterial_thrombosis_causing_cyanosis.jpg/1920px-Arterial_thrombosis_causing_cyanosis.jpg) (figure: acute-arterial-thrombosis; [Commons page](https://commons.wikimedia.org/wiki/File:Arterial_thrombosis_causing_cyanosis.jpg))
9. [Contrast-enhanced CT scan demonstrating abdominal aortic aneurysm.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4a/Contrast-enhanced_CT_scan_demonstrating_abdominal_aortic_aneurysm.jpg/1920px-Contrast-enhanced_CT_scan_demonstrating_abdominal_aortic_aneurysm.jpg) (figure: aaa-ct; [Commons page](https://commons.wikimedia.org/wiki/File:Contrast-enhanced_CT_scan_demonstrating_abdominal_aortic_aneurysm.jpg))
10. [Ultrasonography of abdominal aortic aneurysm in sagittal plane, annotated.jpg](https://upload.wikimedia.org/wikipedia/commons/5/5b/Ultrasonography_of_abdominal_aortic_aneurysm_in_sagittal_plane%2C_annotated.jpg) (figure: aaa-ultrasound; [Commons page](https://commons.wikimedia.org/wiki/File:Ultrasonography_of_abdominal_aortic_aneurysm_in_sagittal_plane,_annotated.jpg))
11. [70PerBlockedRtCarotidACT.png](https://upload.wikimedia.org/wikipedia/commons/f/fb/70PerBlockedRtCarotidACT.png) (figure: carotid-stenosis-ct; [Commons page](https://commons.wikimedia.org/wiki/File:70PerBlockedRtCarotidACT.png))
12. [Mesenteriale Ischaemie mit Pneumatosis intestinalis und Gas in Mesenterial- und Lebervenen 80M - CT - 001.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e9/Mesenteriale_Ischaemie_mit_Pneumatosis_intestinalis_und_Gas_in_Mesenterial-_und_Lebervenen_80M_-_CT_-_001.jpg/1920px-Mesenteriale_Ischaemie_mit_Pneumatosis_intestinalis_und_Gas_in_Mesenterial-_und_Lebervenen_80M_-_CT_-_001.jpg) (figure: mesenteric-ischemia-ct; [Commons page](https://commons.wikimedia.org/wiki/File:Mesenteriale_Ischaemie_mit_Pneumatosis_intestinalis_und_Gas_in_Mesenterial-_und_Lebervenen_80M_-_CT_-_001.jpg))
13. [Disekce klasifikace DeBakey a Stanford.png](https://thumb.wikimedia.org/wikipedia/commons/thumb/2/23/Disekce_klasifikace_DeBakey_a_Stanford.png/1920px-Disekce_klasifikace_DeBakey_a_Stanford.png) (figure: dissection-classification; [Commons page](https://commons.wikimedia.org/wiki/File:Disekce_klasifikace_DeBakey_a_Stanford.png))
14. [Descending (Type B Stanford) Aortic Dissection.PNG](https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/Descending_%28Type_B_Stanford%29_Aortic_Dissection.PNG/1920px-Descending_%28Type_B_Stanford%29_Aortic_Dissection.PNG) (figure: type-b-dissection-ct; [Commons page](https://commons.wikimedia.org/wiki/File:Descending_(Type_B_Stanford)_Aortic_Dissection.PNG))
15. [Deep vein thrombosis of the right leg.jpg](https://upload.wikimedia.org/wikipedia/commons/2/21/Deep_vein_thrombosis_of_the_right_leg.jpg) (figure: dvt-leg; [Commons page](https://commons.wikimedia.org/wiki/File:Deep_vein_thrombosis_of_the_right_leg.jpg))
16. [Ultrasonography of deep vein thrombosis of the femoral vein -annotated.jpg](https://upload.wikimedia.org/wikipedia/commons/4/4f/Ultrasonography_of_deep_vein_thrombosis_of_the_femoral_vein_-annotated.jpg) (figure: dvt-ultrasound; [Commons page](https://commons.wikimedia.org/wiki/File:Ultrasonography_of_deep_vein_thrombosis_of_the_femoral_vein_-annotated.jpg))
17. [Chronicvenousinsufficiency.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Chronicvenousinsufficiency.jpg/1920px-Chronicvenousinsufficiency.jpg) (figure: venous-insufficiency-skin; [Commons page](https://commons.wikimedia.org/wiki/File:Chronicvenousinsufficiency.jpg))
18. [Venous ulcer dorsal leg.jpg](https://upload.wikimedia.org/wikipedia/commons/3/38/Venous_ulcer_dorsal_leg.jpg) (figure: venous-ulcer; [Commons page](https://commons.wikimedia.org/wiki/File:Venous_ulcer_dorsal_leg.jpg))
19. [Neuropathic heel ulcer diabetic.jpg](https://upload.wikimedia.org/wikipedia/commons/c/cd/Neuropathic_heel_ulcer_diabetic.jpg) (figure: neuropathic-heel-ulcer; [Commons page](https://commons.wikimedia.org/wiki/File:Neuropathic_heel_ulcer_diabetic.jpg))
20. [Thoracic Outlet Syndrome.png](https://upload.wikimedia.org/wikipedia/commons/9/90/Thoracic_Outlet_Syndrome.png) (figure: thoracic-outlet; [Commons page](https://commons.wikimedia.org/wiki/File:Thoracic_Outlet_Syndrome.png))

### Open operations

21. [Blausen 0172 CarotidEndarterectomy.png](https://upload.wikimedia.org/wikipedia/commons/a/ab/Blausen_0172_CarotidEndarterectomy.png) (figure: cea-illustration; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_0172_CarotidEndarterectomy.png))
22. [Carotid Plaque.jpg](https://upload.wikimedia.org/wikipedia/commons/4/48/Carotid_Plaque.jpg) (figure: carotid-plaque; [Commons page](https://commons.wikimedia.org/wiki/File:Carotid_Plaque.jpg))
23. [Open infrarenal aortic repair model.jpg](https://upload.wikimedia.org/wikipedia/commons/1/13/Open_infrarenal_aortic_repair_model.jpg) (figure: open-aaa-model; [Commons page](https://commons.wikimedia.org/wiki/File:Open_infrarenal_aortic_repair_model.jpg))
24. [Aneurysm endovascular.jpg](https://upload.wikimedia.org/wikipedia/commons/e/e3/Aneurysm_endovascular.jpg) (figure: evar-illustration; [Commons page](https://commons.wikimedia.org/wiki/File:Aneurysm_endovascular.jpg))
25. [TAstent.PNG](https://upload.wikimedia.org/wikipedia/commons/7/73/TAstent.PNG) (figure: thoracic-stent-graft; [Commons page](https://commons.wikimedia.org/wiki/File:TAstent.PNG))
26. [Leriche Syndrom 76w - MRA.jpg](https://upload.wikimedia.org/wikipedia/commons/4/49/Leriche_Syndrom_76w_-_MRA.jpg) (figure: leriche-mra; [Commons page](https://commons.wikimedia.org/wiki/File:Leriche_Syndrom_76w_-_MRA.jpg))
27. [3D Medical Animation Vascular Bypass Grafting.jpg](https://upload.wikimedia.org/wikipedia/commons/2/2c/3D_Medical_Animation_Vascular_Bypass_Grafting.jpg) (figure: leg-bypass; [Commons page](https://commons.wikimedia.org/wiki/File:3D_Medical_Animation_Vascular_Bypass_Grafting.jpg))
28. [Gray440 - Fascial compartments of leg.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8f/Gray440_-_Fascial_compartments_of_leg.svg/1920px-Gray440_-_Fascial_compartments_of_leg.svg.png) (figure: leg-compartments; [Commons page](https://commons.wikimedia.org/wiki/File:Gray440_-_Fascial_compartments_of_leg.svg))
29. [Fasciotomy leg.jpg](https://upload.wikimedia.org/wikipedia/commons/d/da/Fasciotomy_leg.jpg) (figure: fasciotomy-leg; [Commons page](https://commons.wikimedia.org/wiki/File:Fasciotomy_leg.jpg))
30. [Gangrene toes (1).jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6e/Gangrene_toes_%281%29.jpg/1920px-Gangrene_toes_%281%29.jpg) (figure: toe-gangrene; [Commons page](https://commons.wikimedia.org/wiki/File:Gangrene_toes_(1).jpg))
31. [Blausen 0049 ArteriovenousFistula.png](https://upload.wikimedia.org/wikipedia/commons/f/fd/Blausen_0049_ArteriovenousFistula.png) (figure: av-fistula; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_0049_ArteriovenousFistula.png))
32. [Blausen 0050 ArteriovenousGraft.png](https://upload.wikimedia.org/wikipedia/commons/f/f6/Blausen_0050_ArteriovenousGraft.png) (figure: av-graft; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_0050_ArteriovenousGraft.png))
33. [Great saphenous vein.png](https://upload.wikimedia.org/wikipedia/commons/5/51/Great_saphenous_vein.png) (figure: great-saphenous-course; [Commons page](https://commons.wikimedia.org/wiki/File:Great_saphenous_vein.png))
34. [Debakey forceps.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c4/Debakey_forceps.jpg/1920px-Debakey_forceps.jpg) (figure: debakey-forceps; [Commons page](https://commons.wikimedia.org/wiki/File:Debakey_forceps.jpg))

### Endovascular

35. [Femoral endovascular procedure.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/Femoral_endovascular_procedure.jpg/1920px-Femoral_endovascular_procedure.jpg) (figure: femoral-access-procedure; [Commons page](https://commons.wikimedia.org/wiki/File:Femoral_endovascular_procedure.jpg))
36. [Catheter Schema 2 pose du fil.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/d/db/Catheter_Schema_2_pose_du_fil.svg/1920px-Catheter_Schema_2_pose_du_fil.svg.png) (figure: seldinger-wire; [Commons page](https://commons.wikimedia.org/wiki/File:Catheter_Schema_2_pose_du_fil.svg))
37. [Catheterization selective angiography.JPG](https://upload.wikimedia.org/wikipedia/commons/2/2b/Catheterization_selective_angiography.JPG) (figure: selective-angiography; [Commons page](https://commons.wikimedia.org/wiki/File:Catheterization_selective_angiography.JPG))
38. [IVUS of CAD.png](https://upload.wikimedia.org/wikipedia/commons/a/a5/IVUS_of_CAD.png) (figure: ivus-coronary; [Commons page](https://commons.wikimedia.org/wiki/File:IVUS_of_CAD.png))
39. [Hybrid operating theatre gemelli rome.jpg](https://upload.wikimedia.org/wikipedia/commons/0/07/Hybrid_operating_theatre_gemelli_rome.jpg) (figure: hybrid-or; [Commons page](https://commons.wikimedia.org/wiki/File:Hybrid_operating_theatre_gemelli_rome.jpg))
40. [Abdominal CT angiography.jpg](https://upload.wikimedia.org/wikipedia/commons/a/a1/Abdominal_CT_angiography.jpg) (figure: ct-angiography; [Commons page](https://commons.wikimedia.org/wiki/File:Abdominal_CT_angiography.jpg))
41. [Angioplasty-scheme.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/6/68/Angioplasty-scheme.svg/1920px-Angioplasty-scheme.svg.png) (figure: angioplasty-scheme; [Commons page](https://commons.wikimedia.org/wiki/File:Angioplasty-scheme.svg))
42. [Angioplasty - Balloon Inflated with Stent.png](https://upload.wikimedia.org/wikipedia/commons/8/87/Angioplasty_-_Balloon_Inflated_with_Stent.png) (figure: balloon-stent; [Commons page](https://commons.wikimedia.org/wiki/File:Angioplasty_-_Balloon_Inflated_with_Stent.png))
43. [Blausen Atherectomy eng.svg](https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6f/Blausen_Atherectomy_eng.svg/1920px-Blausen_Atherectomy_eng.svg.png) (figure: atherectomy, atherectomy-devices; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_Atherectomy_eng.svg))
44. [Endovasc.jpg](https://upload.wikimedia.org/wikipedia/commons/9/95/Endovasc.jpg) (figure: evar-ct; [Commons page](https://commons.wikimedia.org/wiki/File:Endovasc.jpg))
45. [AAA-X4.jpg](https://upload.wikimedia.org/wikipedia/commons/a/a3/AAA-X4.jpg) (figure: aaa-neck-anatomy; [Commons page](https://commons.wikimedia.org/wiki/File:AAA-X4.jpg))
46. [ArtistsFenBranchInSituCropped.jpg](https://upload.wikimedia.org/wikipedia/commons/0/0a/ArtistsFenBranchInSituCropped.jpg) (figure: fenestrated-branched; [Commons page](https://commons.wikimedia.org/wiki/File:ArtistsFenBranchInSituCropped.jpg))
47. [Angiograph before and after thrombolytic therapy in a case of thrombosis on the hand.png](https://upload.wikimedia.org/wikipedia/commons/2/2e/Angiograph_before_and_after_thrombolytic_therapy_in_a_case_of_thrombosis_on_the_hand.png) (figure: thrombolysis-angiogram; [Commons page](https://commons.wikimedia.org/wiki/File:Angiograph_before_and_after_thrombolytic_therapy_in_a_case_of_thrombosis_on_the_hand.png))
48. [Aneurysma spurium Arteria profunda femoris - 80jw - DSA Coiling - 001.jpg](https://upload.wikimedia.org/wikipedia/commons/b/bb/Aneurysma_spurium_Arteria_profunda_femoris_-_80jw_-_DSA_Coiling_-_001.jpg) (figure: pseudoaneurysm-coiling; [Commons page](https://commons.wikimedia.org/wiki/File:Aneurysma_spurium_Arteria_profunda_femoris_-_80jw_-_DSA_Coiling_-_001.jpg))
49. [IVCFilterMark.png](https://upload.wikimedia.org/wikipedia/commons/7/79/IVCFilterMark.png) (figure: ivc-filter-xray; [Commons page](https://commons.wikimedia.org/wiki/File:IVCFilterMark.png))
50. [Radial artery pseudaneurysm 20180607b.jpg](https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Radial_artery_pseudaneurysm_20180607b.jpg/1920px-Radial_artery_pseudaneurysm_20180607b.jpg) (figure: radial-pseudoaneurysm; [Commons page](https://commons.wikimedia.org/wiki/File:Radial_artery_pseudaneurysm_20180607b.jpg))
51. [Herzkatheterlabor modern.jpeg](https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f3/Herzkatheterlabor_modern.jpeg/1920px-Herzkatheterlabor_modern.jpeg) (figure: cath-lab; [Commons page](https://commons.wikimedia.org/wiki/File:Herzkatheterlabor_modern.jpeg))

### Devices

52. [Seldinger Set.jpg](https://upload.wikimedia.org/wikipedia/commons/6/6e/Seldinger_Set.jpg) (figure: seldinger-set; [Commons page](https://commons.wikimedia.org/wiki/File:Seldinger_Set.jpg))
53. [Introducer sheaths.jpg](https://upload.wikimedia.org/wikipedia/commons/1/1d/Introducer_sheaths.jpg) (figure: introducer-sheaths; [Commons page](https://commons.wikimedia.org/wiki/File:Introducer_sheaths.jpg))
54. [Balloon-Tipped Catheter.png](https://upload.wikimedia.org/wikipedia/commons/5/5c/Balloon-Tipped_Catheter.png) (figure: balloon-catheter; [Commons page](https://commons.wikimedia.org/wiki/File:Balloon-Tipped_Catheter.png))
55. [Stent4 (fcm).jpg](https://upload.wikimedia.org/wikipedia/commons/0/07/Stent4_%28fcm%29.jpg) (figure: stents-photo; [Commons page](https://commons.wikimedia.org/wiki/File:Stent4_(fcm).jpg))
56. [FenGraft.jpg](https://upload.wikimedia.org/wikipedia/commons/2/2a/FenGraft.jpg) (figure: fenestrated-graft; [Commons page](https://commons.wikimedia.org/wiki/File:FenGraft.jpg))
57. [Blausen 0024 Angiojet.png](https://upload.wikimedia.org/wikipedia/commons/f/f4/Blausen_0024_Angiojet.png) (figure: angiojet; [Commons page](https://commons.wikimedia.org/wiki/File:Blausen_0024_Angiojet.png))
58. [Inferior vena cava filter.jpg](https://upload.wikimedia.org/wikipedia/commons/d/d2/Inferior_vena_cava_filter.jpg) (figure: ivc-filter-device; [Commons page](https://commons.wikimedia.org/wiki/File:Inferior_vena_cava_filter.jpg))
59. [Vascular closure device.jpg](https://upload.wikimedia.org/wikipedia/commons/e/e2/Vascular_closure_device.jpg) (figure: radial-compression; [Commons page](https://commons.wikimedia.org/wiki/File:Vascular_closure_device.jpg))
60. [CO2 angiography.jpg](https://upload.wikimedia.org/wikipedia/commons/b/b1/CO2_angiography.jpg) (figure: co2-angiography; [Commons page](https://commons.wikimedia.org/wiki/File:CO2_angiography.jpg))
