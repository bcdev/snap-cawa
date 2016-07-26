package org.esa.snap.dataio.nc4;

import org.esa.snap.core.dataio.EncodeQualification;
import org.esa.snap.core.datamodel.*;
import org.esa.snap.core.image.ImageManager;
import org.esa.snap.dataio.netcdf.AbstractNetCdfWriterPlugIn;
import org.esa.snap.dataio.netcdf.ProfileWriteContext;
import org.esa.snap.dataio.netcdf.metadata.ProfileInitPartWriter;
import org.esa.snap.dataio.netcdf.metadata.ProfilePartWriter;
import org.esa.snap.dataio.netcdf.metadata.profiles.beam.BeamFlagCodingPart;
import org.esa.snap.dataio.netcdf.metadata.profiles.beam.BeamGeocodingPart;
import org.esa.snap.dataio.netcdf.metadata.profiles.beam.BeamTiePointGridPart;
import org.esa.snap.dataio.netcdf.nc.NFileWriteable;
import org.esa.snap.dataio.netcdf.nc.NVariable;
import org.esa.snap.dataio.netcdf.nc.NWritableFactory;
import org.esa.snap.dataio.netcdf.util.DataTypeUtils;

import java.awt.*;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;
import java.util.UUID;

/**
 * Writer plugin for NetCDF4 output adapted to SNAP CAWA requirements (i.e. specific metadata)
 *
 * @author olafd
 */
public class SnapCawaNc4WriterPlugIn extends AbstractNetCdfWriterPlugIn {

    public String[] getFormatNames() {
        return new String[]{"NetCDF4-CAWA"};
    }

    public String[] getDefaultFileExtensions() {
        return new String[]{".nc"};
    }

    public String getDescription(Locale locale) {
        return "SNAP CAWA NetCDF4 products";
    }

    @Override
    public ProfilePartWriter createFlagCodingPartWriter() {
        return new BeamFlagCodingPart();
    }

    @Override
    public ProfilePartWriter createTiePointGridPartWriter() {
        return new BeamTiePointGridPart();
    }


    @Override
    public ProfilePartWriter createGeoCodingPartWriter() {
//        return new BeamGeocodingPart();
        return new SnapCawaGeocodingPart();
    }

    @Override
    public ProfileInitPartWriter createInitialisationPartWriter() {
        return new SnapCawaMainPart();
    }

    @Override
    public NFileWriteable createWritable(String outputPath) throws IOException {
        return NWritableFactory.create(outputPath, "netcdf4");
    }

    public EncodeQualification getEncodeQualification(Product product) {
        if (product.isMultiSize()) {
            return new EncodeQualification(EncodeQualification.Preservation.UNABLE,
                                           "Cannot write multisize products. Consider resampling the product first.");
        }
        return new EncodeQualification(EncodeQualification.Preservation.PARTIAL);
    }

    private class SnapCawaMainPart implements ProfileInitPartWriter {

        private final SimpleDateFormat COMPACT_ISO_FORMAT = new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'");
        private Dimension tileSize;

        SnapCawaMainPart() {
            COMPACT_ISO_FORMAT.setTimeZone(TimeZone.getTimeZone("UTC"));
        }

        public void writeProductBody(ProfileWriteContext ctx, Product product) throws IOException {
            // todo: maybe we should use a sensor config when we deal with all AVHRR sensors
//            String sensor = product.getMetadataRoot().getAttributeString("sensor");
//            String spatialResolution = product.getMetadataRoot().getAttributeString("spatialResolution");
//            if (sensorConfig == null) {
//                sensorConfig = AvhrrAcSensorConfig.create(sensor, spatialResolution);
//            }

            NFileWriteable writeable = ctx.getNetcdfFileWriteable();
            tileSize = ImageManager.getPreferredTileSize(product);

            // writeable.addDimension("time", 1);  todo: do we want this??
            writeable.addDimension("y", product.getSceneRasterHeight());
            writeable.addDimension("x", product.getSceneRasterWidth());

//            addGlobalAttributes(writeable, product);

            for (Band b : product.getBands()) {
                final String bandName = b.getName();
                if (bandName.equals("tcwv")) {
                    addNc4VariableAttribute(writeable, b,
                            Nc4Constants.AC_CORR_VALID_MIN_VALUE, Nc4Constants.AC_CORR_VALID_MAX_VALUE);

                } else if (bandName.endsWith("flags")) {
                    addNc4VariableAttribute(writeable, b,
                            Nc4Constants.UNCERTAINTY_VALID_MIN_VALUE, Nc4Constants.UNCERTAINTY_VALID_MAX_VALUE);
                } else {
                    // all other bands
//                    addAcAncillaryVariableAttributes(writeable, b);
                }
            }

        }

        private void addAcAncillaryVariableAttributes(NFileWriteable writeable, Band b) throws IOException {
            if (b.getName().equals(Nc4Constants.LAT_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.LAT_VALID_MIN_VALUE, Nc4Constants.LAT_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.LON_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.LON_VALID_MIN_VALUE, Nc4Constants.LON_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.SZA_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.SZA_VALID_MIN_VALUE, Nc4Constants.SZA_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.SAA_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.SAA_VALID_MIN_VALUE, Nc4Constants.SAA_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.VZA_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.VZA_VALID_MIN_VALUE, Nc4Constants.VZA_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.VAA_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.VAA_VALID_MIN_VALUE, Nc4Constants.VAA_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.QUALITY_FLAG_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.QUALITY_VALID_MIN_VALUE, Nc4Constants.QUALITY_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.GROUD_HEIGHT_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.GROUND_HEIGHT_VALID_MIN_VALUE, Nc4Constants.GROUND_HEIGHT_VALID_MAX_VALUE);
            } else if (b.getName().equals(Nc4Constants.NDVI_BAND_NAME)) {
                addNc4VariableAttribute(writeable, b, Nc4Constants.NDVI_VALID_MIN_VALUE, Nc4Constants.NDVI_VALID_MAX_VALUE);
            } else {
                // the optional debug bands
                addNc4VariableAttribute(writeable, b, Double.MIN_VALUE, Double.MAX_VALUE);
            }
        }

        private void addGlobalAttributes(NFileWriteable writeable, Product product) throws IOException {

            // global attributes
            final MetadataElement srcGaRoot =
                    product.getMetadataRoot().getElement("Global_Attributes_Reflectance_Product");
            final MetadataElement cmGaRoot =
                    product.getMetadataRoot().getElement("Global_Attributes_CM");
            final MetadataElement wmGaRoot =
                    product.getMetadataRoot().getElement("Global_Attributes_WM");

            final String srcId = getAttributeString(srcGaRoot, "id");

            writeable.addGlobalAttribute("title", "AVHRR-SDR-L2 product in satellite projection");
            writeable.addGlobalAttribute("institution", "DLR-EOC-DFD");
            writeable.addGlobalAttribute("creator_name", "Corinne Frey");
            writeable.addGlobalAttribute("creator_url", "http://www.dlr.de/eoc");
            writeable.addGlobalAttribute("creator_email", "timeline@dlr.de");
            writeable.addGlobalAttribute("project", "timeline");
            writeable.addGlobalAttribute("naming_authority", "dlr.dfd.de");
            writeable.addGlobalAttribute("history", "");
            writeable.addGlobalAttribute("references", "http://www.timeline.dlr.de'");
            writeable.addGlobalAttribute("DOI", "10.15489/wnqagxbpsa75");  // todo: set DOI = 10.15489/pxwtbx619j71 when we have SR product
            writeable.addGlobalAttribute("Conventions", "CF-1.6, Unidata Observation Dataset v1.1");
            writeable.addGlobalAttribute("standard_name_vocabulary", "NetCDF Climate and Forecast (CF) Metadata Convenstion version 1.6");
            writeable.addGlobalAttribute("netcdf_version_id", "4.0");
            writeable.addGlobalAttribute("cdm_data_type", "Swath");
            writeable.addGlobalAttribute("processing_level", "L2");
            writeable.addGlobalAttribute("product_version", "01.01");
            writeable.addGlobalAttribute("processor_versions", "");
            writeable.addGlobalAttribute("license", "All intellectual property rights of the TIMELINE products belong " +
                    "to EOC-DLR. The use of these products is granted to everybody free of charge, following " +
                    "TIMELINEs free and open data policy. Please refer to the TIMELINE data policy for reference " +
                    "and copyright credit specifications.");
            writeable.addGlobalAttribute("summary", "This dataset contains L2 reflectance data from the AVHRR sensor produced in the TIMELINE project.");
            writeable.addGlobalAttribute("keywords", "Earth Science, Land Surface, Surface Radiative Properties");
            writeable.addGlobalAttribute("keywords_vocabulary", "NASA Global Change Master Directory (GCMD) Science Keywords");
            writeable.addGlobalAttribute("source", "");
            writeable.addGlobalAttribute("platform", "");
            writeable.addGlobalAttribute("sensor", "");
            writeable.addGlobalAttribute("comment", "-");
            writeable.addGlobalAttribute("code", "TL.AVHRR.L2_SDR");
            writeable.addGlobalAttribute("uuid", UUID.randomUUID().toString());
            writeable.addGlobalAttribute("id", srcId.replace("-L1B-", "-L2-SDR-"));
            writeable.addGlobalAttribute("date_created", COMPACT_ISO_FORMAT.format(new Date()));
            setInputComponentsAttribute(writeable, srcGaRoot, cmGaRoot, wmGaRoot);
            writeable.addGlobalAttribute("spatial_resolution", "");
        }

        private void setInputComponentsAttribute(NFileWriteable writeable,
                                                 MetadataElement srcGaRoot,
                                                 MetadataElement cmGaRoot,
                                                 MetadataElement wmGaRoot) throws IOException {
            final String srcInputComponents = getAttributeString(srcGaRoot, "input_components");
            final String srcId = getAttributeString(srcGaRoot, "id");
            final String cmInputComponents = getAttributeString(cmGaRoot, "input_components");
            final String cmId = getAttributeString(cmGaRoot, "id");
            final String wmInputComponents = getAttributeString(wmGaRoot, "input_components");
            final String wmId = getAttributeString(wmGaRoot, "id");

            String resultInputComponents = srcInputComponents;
            if (!resultInputComponents.contains(cmInputComponents)) {
                resultInputComponents = resultInputComponents.concat("; ").concat(cmInputComponents);
            }
            if (!resultInputComponents.contains(wmInputComponents)) {
                resultInputComponents = resultInputComponents.concat("; ").concat(wmInputComponents);
            }
            resultInputComponents = resultInputComponents.concat("; ").concat(srcId);
            resultInputComponents = resultInputComponents.concat("; ").concat(cmId);
            resultInputComponents = resultInputComponents.concat("; ").concat(wmId);

            writeable.addGlobalAttribute("input_components", resultInputComponents);
        }

        private String getAttributeString(MetadataElement parent, String name) {
            final MetadataAttribute attr = parent.getAttribute(name);
            final ProductData attrData = attr != null ? attr.getData() : null;
            return attrData != null ? attrData.getElemString() : "";
        }

        private void addNc4VariableAttribute(NFileWriteable writeable, RasterDataNode b,
                                             double validMinValue,
                                             double validMaxValue) throws IOException {
            NVariable variable = writeable.addVariable(b.getName(),
                                                       DataTypeUtils.getNetcdfDataType(b.getDataType()),
                                                       tileSize, writeable.getDimensions());

//            final String bandName = b.getName();
//            String longName;
//            String standardName;
//            String coverageContentType;
//            if (bandName.startsWith("avhrr") && bandName.endsWith("ac")) {
//                // AC reflectance band
//                longName = "surface_directional_reflectance_of_channel_" + bandName.split("_")[1];
//                standardName = "surface_bidirectional_reflectance";
//                coverageContentType = "physicalMeasurement";
//            } else if (bandName.startsWith("avhrr") && bandName.endsWith("uncertainty")) {
//                // AC reflectance uncertainty band
//                longName = "uncertainty_of_surface_directional_reflectance_of_channel_" + bandName.split("_")[1];
//                standardName = "surface_bidirectional_reflectance standard_error";
//                coverageContentType = "auxiliaryInformation";
//            } else {
//                final String desrc = b.getDescription();
//                longName = desrc != null && desrc.length() > 0 ? desrc : b.getName();
//                standardName = b.getName();
//                coverageContentType = "auxiliaryInformation";
//            }
//
//            variable.addAttribute("long_name", longName);
//            variable.addAttribute("standard_name", standardName);
//            variable.addAttribute("description", "-");
//            variable.addAttribute("fill_value", b.getNoDataValue());
//            variable.addAttribute("valid_min", validMinValue);
//            variable.addAttribute("valid_max", validMaxValue);
//            variable.addAttribute("scale_factor", b.getScalingFactor());
//            variable.addAttribute("add_offset", b.getScalingOffset());
//            variable.addAttribute("units", b.getUnit());
//            variable.addAttribute("coverage_content_type", coverageContentType);
        }
    }


}
