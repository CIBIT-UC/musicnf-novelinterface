# Defacer to share the dataset

I am using this bids app:https://github.com/PeerHerholz/BIDSonym

## Single participant
```bash
docker run -i --rm \
            -v /Volumes/T7/BIDS-MUSICNF:/bids_dataset \
            peerherholz/bidsonym \
            /bids_dataset \
            participant \
            --deid pydeface \
            --del_meta 'InstitutionName' 'InstitutionalDepartmentName' 'InstitutionAddress' 'ProcedureStepDescription' \
            --participant_label 01 \
            --brainextraction bet --bet_frac 0.5 \
            --deface_t2w \
            --skip_bids_validation

```

does not work what